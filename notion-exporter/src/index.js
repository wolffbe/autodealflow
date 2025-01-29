import { connectToRedis } from './redis_client.js';
import { canAccessNotionPage, createNotionDatabase, updateDatabaseColumns, addRowToDatabase } from './notion.js';
import { now } from './utils.js';
import config from './config.js';
import logger from './logger.js';

async function runNotionExporter() {
    try {
        logger.debug('Connecting to Redis...');
        const redis = await connectToRedis();
        logger.debug('Checking access to Notion page...');
        await canAccessNotionPage(config.notionDbParentPageId);

        logger.info('Starting notion exporter...');

        const databaseId = await createNotionDatabase(config.notionDbParentPageId, now());
        logger.debug(`Notion database created with ID: ${databaseId}`);

        await updateDatabaseColumns(databaseId, config.oppFields);
        logger.debug('Database columns updated successfully.');

        while (true) {
            try {
                logger.debug('Waiting for new messages in Redis...');
                const [queue, message] = await redis.blpop(config.notionExportCh, 0);
                const msgJson = JSON.parse(message);

                logger.debug(`Received export message with ID '${msgJson.id}'`);

                await addRowToDatabase(databaseId, msgJson.fields);
                logger.info(`Processed export message with ID '${msgJson.id}'`);
            } catch (error) {
                throw new Error(`Error processing message in exporter: ${error.message}`);
            }
        }
    } catch (error) {
        throw new Error(`Error running Notion Exporter: ${error.message}`);
    }
}

runNotionExporter();