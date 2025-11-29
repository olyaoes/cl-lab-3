const { app } = require('@azure/functions');
const { QueueClient } = require('@azure/storage-queue');

app.http('IngestSensorData', {
    methods: ['POST'],
    authLevel: 'anonymous',
    handler: async (request, context) => {
        try {
            const body = await request.json();
            context.log("Received data:", body);

            const connStr = process.env["AzureWebJobsStorage"];
            const queueName = "sensor-data-queue";

            const queueClient = new QueueClient(connStr, queueName);

            await queueClient.createIfNotExists();

            const message = Buffer.from(JSON.stringify(body)).toString("base64");

            await queueClient.sendMessage(message);

            return {
                status: 200,
                jsonBody: { ok: true, queued: body }
            };

        } catch (err) {
            context.log("ERROR:", err);
            return {
                status: 500,
                jsonBody: { error: err.message }
            };
        }
    }
});
