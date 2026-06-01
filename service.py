"""
Background service for Android to keep the load tester running
even when the app is in the background
"""

import os
import sys
import time
from jnius import autoclass

# Android imports
PythonService = autoclass('org.kivy.android.PythonService')
PythonService.mService.setAutoRestartService(True)

# Notification for foreground service
Context = autoclass('android.content.Context')
NotificationBuilder = autoclass('android.app.Notification$Builder')
NotificationChannel = autoclass('android.app.NotificationChannel')
NotificationManager = autoclass('android.app.NotificationManager')
PendingIntent = autoclass('android.app.PendingIntent')
Intent = autoclass('android.content.Intent')

def create_notification():
    """Create a notification for the foreground service"""
    service = PythonService.mService
    
    # Create notification channel (required for Android 8.0+)
    channel_id = "loadtester_service"
    channel = NotificationChannel(
        channel_id,
        "Load Tester Service",
        NotificationManager.IMPORTANCE_LOW
    )
    
    notification_service = service.getSystemService(Context.NOTIFICATION_SERVICE)
    notification_service.createNotificationChannel(channel)
    
    # Create notification
    builder = NotificationBuilder(service, channel_id)
    builder.setContentTitle("Load Tester")
    builder.setContentText("Running in background...")
    builder.setSmallIcon(service.getApplicationInfo().icon)
    
    # Create intent to open app when notification is clicked
    intent = Intent(service, PythonService)
    pending_intent = PendingIntent.getActivity(service, 0, intent, 0)
    builder.setContentIntent(pending_intent)
    
    return builder.build()

def main():
    """Main service loop"""
    # Start foreground service with notification
    notification = create_notification()
    PythonService.mService.startForeground(1, notification)
    
    # Keep service alive
    while True:
        time.sleep(60)  # Check every minute
        
        # Service will keep running as long as the main app needs it
        # The actual load testing runs in the main app's threads

if __name__ == '__main__':
    main()
