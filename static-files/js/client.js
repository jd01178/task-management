// client.js
// Replace with your server URL

// Function to subscribe to push notifications
async function subscribeToPushNotifications() {
  try {
    const registration = await navigator.serviceWorker.register('/static/navigatorPush.service.js');
    const subscription = await registration.pushManager.subscribe({ userVisibleOnly: true });
    const response = await sendPostRequest('/api/v1/subscribe/', {
        registration_id: subscription.endpoint,
        device_type: 'web',  // or 'android' for Android devices, 'ios' for iOS devices
    })
    if (response.ok) {
      console.log('Subscription successful!');
    } else {
      console.error('Subscription failed:', response.status, response.statusText);
    }
  } catch (error) {
    console.error('Error during subscription:', error);
  }
}

// Call the function to subscribe
subscribeToPushNotifications();
