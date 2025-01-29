import { formatAsUUID } from "./utils.js";

const requiredEnvVars = [
  "LOG_LEVEL",
  "REDIS_HOST",
  "REDIS_PORT",
  "NOTION_EXPORT_CH",
  "NOTION_API_KEY",
  "NOTION_DB_PARENT_PAGE_ID",
  "OPP_FIELDS",
];

const missingVars = requiredEnvVars.filter((varName) => !process.env[varName]);

if (missingVars.length > 0) {
  throw new Error(`Missing required environment variables: ${missingVars.join(", ")}`);
}

const validLogLevels = ["INFO", "DEBUG"];
const logLevel = process.env.LOG_LEVEL;

if (!validLogLevels.includes(logLevel)) {
  throw new Error(`Invalid LOG_LEVEL value. It must be one of: ${validLogLevels.join(", ")}`);
}

const notionDbParentPageId = process.env.NOTION_DB_PARENT_PAGE_ID;

if (!notionDbParentPageId) {
  throw new Error("NOTION_DB_PARENT_PAGE_ID environment variable is missing.");
}

let formattedNotionDbParentPageId;
try {
  formattedNotionDbParentPageId = formatAsUUID(notionDbParentPageId);
} catch (e) {
  throw new Error(`Error formatting Notion DB Parent Page ID: ${e.message}`);
}

export default {
  logLevel,
  redisHost: process.env.REDIS_HOST,
  redisPort: process.env.REDIS_PORT,
  notionExportCh: process.env.NOTION_EXPORT_CH,
  notionApiKey: process.env.NOTION_API_KEY,
  notionDbParentPageId: formattedNotionDbParentPageId,
  oppFields: process.env.OPP_FIELDS,
};