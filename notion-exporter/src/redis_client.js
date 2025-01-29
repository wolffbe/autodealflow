import Redis from 'ioredis';
import logger from './logger.js';
import config from './config.js';

export async function connectToRedis() {
  try {
    if (!config.redisHost || !config.redisPort) {
      throw new Error('Redis host or port not defined in config.');
    }

    logger.debug('Connecting to Redis...');

    const client = new Redis({
      host: config.redisHost,
      port: config.redisPort,
      retryStrategy(times) {
        return Math.min(times * 50, 2000);
      },
      connectTimeout: 5000,
    });

    client.on('error', (err) => {
      throw new Error('Redis Client Error: ' + err.message);
    });

    client.on('connect', () => {
      logger.debug('Redis client is connecting...');
    });

    client.on('ready', () => {
      logger.debug('Redis client is ready and connected.');
    });

    client.on('end', () => {
      logger.debug('Redis client has ended the connection.');
    });

    logger.debug('Redis client connected successfully');
    return client;
  } catch (err) {
    throw new Error('Error connecting to Redis: ' + err.message);
  }
}