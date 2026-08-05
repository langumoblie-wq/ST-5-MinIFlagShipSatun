import sys

with open('src/lib/gasDb.ts', 'r') as f:
    content = f.read()

old_format_row = """const formatRowIn = (data: any) => {
  if (!data) return data;
  const payload = { ...data };
  try {
      if (payload.timestamp && typeof payload.timestamp === 'number') {
        payload.timestamp = formatDateForSheet(payload.timestamp);
      }
      if (payload.createdAt && typeof payload.createdAt === 'number') {
        payload.createdAt = formatDateForSheet(payload.createdAt);
      }
  } catch (err) {
      console.error("formatRowIn error:", err, data);
  }
  return payload;
};"""

new_format_row = """const formatRowIn = (data: any) => {
  if (!data) return data;
  return { ...data };
};"""

if old_format_row in content:
    content = content.replace(old_format_row, new_format_row)
    print("Replaced formatRowIn in gasDb.ts")

with open('src/lib/gasDb.ts', 'w') as f:
    f.write(content)

with open('src/App.tsx', 'r') as f:
    content_app = f.read()

old_sync = """    if (formattedPayload.timestamp) {
      formattedPayload.timestamp = formatDate(formattedPayload.timestamp);
    }
    if (formattedPayload.createdAt) {
      formattedPayload.createdAt = formatDate(formattedPayload.createdAt);
    }"""

new_sync = """    // Let Apps Script handle the date formatting natively"""

if old_sync in content_app:
    content_app = content_app.replace(old_sync, new_sync)
    print("Replaced sync in App.tsx")

with open('src/App.tsx', 'w') as f:
    f.write(content_app)

