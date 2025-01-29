export function formatAsUUID(input) {
  let cleaned = input;

  if (input.includes('-')) {
    cleaned = input.substring(input.indexOf('-') + 1);
  }

  const hexOnly = cleaned.replace(/[^a-fA-F0-9]/g, '').substring(0, 32);

  if (hexOnly.length !== 32) {
    throw new Error('Invalid input: must have 32 hex characters');
  }

  if (/^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$/.test(input)) {
    return input;
  }

  return `${hexOnly.substring(0, 8)}-${hexOnly.substring(8, 12)}-${hexOnly.substring(12, 16)}-${hexOnly.substring(16, 20)}-${hexOnly.substring(20)}`;
}

export function now() {
  const currentTime = new Date();
  const formattedTime = `${currentTime.getFullYear()}-${(currentTime.getMonth() + 1).toString().padStart(2, '0')}-${currentTime.getDate().toString().padStart(2, '0')} ${currentTime.getHours().toString().padStart(2, '0')}:${currentTime.getMinutes().toString().padStart(2, '0')}:${currentTime.getSeconds().toString().padStart(2, '0')}`;

  return formattedTime;
}