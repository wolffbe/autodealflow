import config from './config.js';
import { Client } from '@notionhq/client';
import logger from './logger.js';

const notion = new Client({ auth: config.notionApiKey });

export async function canAccessNotionPage(pageId) {
    try {
        await notion.pages.retrieve({ page_id: pageId });
        logger.debug(`Page accessed successfully: ${pageId}`);
        return true;
    } catch (error) {
        if (error.code === 'object_not_found') {
            throw new Error('Page not found: ' + error.message);
        } else if (error.code === 'unauthorized') {
            throw new Error('Unauthorized access: ' + error.message);
        } else {
            throw new Error('Unknown error: ' + error.message);
        }
    }
}

export async function createNotionDatabase(parentPageId, databaseTitle) {
    try {
        logger.debug(`Creating database titled '${databaseTitle}' under parent page ID: ${parentPageId}`);
        const response = await notion.databases.create({
            parent: { page_id: parentPageId },
            title: [
                {
                    type: 'text',
                    text: {
                        content: databaseTitle,
                    },
                },
            ],
            properties: {
                Name: {
                    title: {},
                },
                Description: {
                    rich_text: {},
                },
            },
        });
        logger.debug(`Database created successfully with ID: ${response.id}`);
        return response.id;
    } catch (error) {
        throw new Error('Error creating Notion database: ' + error.message);
    }
}

function formatProperties(fields) {
    const fieldNames = fields.split(';').map(field => field.trim());
    const properties = {};

    fieldNames.forEach(fieldName => {
        properties[fieldName] = {
            rich_text: {},
        };
    });

    return properties;
}

export async function updateDatabaseColumns(databaseId, fields) {
    try {
        logger.debug(`Updating columns for database ID: ${databaseId}`);
        const properties = formatProperties(fields);

        await notion.databases.update({
            database_id: databaseId,
            properties: properties,
        });
        logger.debug(`Columns updated successfully for database ID: ${databaseId}`);
    } catch (error) {
        throw new Error('Error updating Notion database columns: ' + error.message);
    }
}

export async function addRowToDatabase(databaseId, rowData) {
    try {
        logger.debug(`Adding row to database ID: ${databaseId}`);
        const properties = {};

        for (const [field, value] of Object.entries(rowData)) {
            if (value !== undefined && value !== null) {
                properties[field] = {
                    rich_text: [
                        {
                            text: {
                                content: value.toString(),
                            },
                        },
                    ],
                };
            }
        }

        const response = await notion.pages.create({
            parent: { database_id: databaseId },
            properties: properties,
        });

        logger.debug(`Row added successfully with ID: ${response.id}`);
        return response;
    } catch (error) {
        throw new Error('Error adding row to Notion database: ' + error.message);
    }
}