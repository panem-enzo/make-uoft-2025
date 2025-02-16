#include "esp_camera.h"
#include <WiFi.h>
#include <WiFiClientSecure.h>

// Wifi Hotspot
const char* ssid = "enzop";
const char* password = "makeuoft2025";

const char* cloudflareWorkerURL = "https://615c250b-cloudflare-worker.panemjf.workers.dev/";

WiFiServer server(80);

void setupCamera() {
    camera_config_t config;
    Serial.printf("PSRAM Size: %d bytes\n", ESP.getPsramSize());
    Serial.printf("Free PSRAM: %d bytes\n", ESP.getFreePsram());

    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = 11;
    config.pin_d1 = 9;
    config.pin_d2 = 8;
    config.pin_d3 = 10;
    config.pin_d4 = 12;
    config.pin_d5 = 18;
    config.pin_d6 = 17;
    config.pin_d7 = 16;
    config.pin_xclk = 15;
    config.pin_pclk = 13;
    config.pin_vsync = 6;
    config.pin_href = 7;
    config.pin_sscb_sda = 4;
    config.pin_sscb_scl = 5;
    config.pin_pwdn = -1;
    config.pin_reset = -1;
    config.xclk_freq_hz = 20000000;
    config.frame_size = FRAMESIZE_CIF; // FRAMESIZE_SVGA
    config.pixel_format = PIXFORMAT_JPEG;
    config.fb_location = CAMERA_FB_IN_PSRAM; // Use PSRAM
    config.jpeg_quality = 12;
    config.fb_count = 2;

    if (psramFound()){
        config.jpeg_quality = 10;
        config.fb_count = 2;
        config.grab_mode = CAMERA_GRAB_LATEST;
    } else {
        // Limit the frame size when PSRAM is not available
        config.fb_count = 1;
        config.fb_location = CAMERA_FB_IN_DRAM;
    }

    if (esp_camera_init(&config) != ESP_OK) {
        Serial.println("Camera Init Failed");
        while (true);
    }
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }
    Serial.println("\nWiFi Connected!");

    setupCamera();
    server.begin();
    Serial.println("MJPEG Stream Ready: http://172.20.10.10/");
}

void loop() {
    WiFiClient client = server.available();
    if (client) {
        Serial.println("Client Connected");

        client.println("HTTP/1.1 200 OK");
        client.println("Content-Type: multipart/x-mixed-replace; boundary=frame");
        client.println();

        while (client.connected()) {
            camera_fb_t *fb = esp_camera_fb_get();
            if (!fb) continue;

            client.println("--frame");
            client.println("Content-Type: image/jpeg");
            client.print("Content-Length: ");
            client.println(fb->len);
            client.println();
            client.write(fb->buf, fb->len);
            client.println();

            esp_camera_fb_return(fb);
            delay(100); // Adjust for frame rate
        }
        client.stop();
        Serial.println("Client Disconnected");
    }
}
