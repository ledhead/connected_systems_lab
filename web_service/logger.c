/**
 * This file handles subscription to the motion detection event via Axis VMD3
 */

#include <glib.h>
#include <glib-object.h>
#include <axsdk/axevent.h>
#include <syslog.h>
#include <stdio.h>
#include <time.h>

static void
subscription_callback(guint subscription,
    AXEvent *event, FILE *fp);

static guint
subscribe_to_motion_detection_event(AXEventHandler *event_handler, FILE *fp);

static void
subscription_callback(guint subscription,
    AXEvent *event, FILE *fp)
{
  const AXEventKeyValueSet *key_value_set;
  gboolean active;
  time_t cur_time;
  struct tm *time_info;

  (void)subscription;

  key_value_set = ax_event_get_key_value_set(event);

  ax_event_key_value_set_get_boolean(key_value_set,
        "active", NULL, &active, NULL);

  time(&cur_time); 
  time_info = localtime (&cur_time);

  if (active) {
    syslog(LOG_INFO, "Motion detected");
    g_message("Motion detected: %s is high", asctime(time_info));
    fprintf(fp, "Motion detected: %s", asctime(time_info));  
  } else {
    syslog(LOG_INFO, "Motion not detected");
    g_message("Motion not detected: %s is high", asctime(time_info));
    fprintf(fp, "Motion no longer detected: %s", asctime(time_info));
  }
}

static guint
subscribe_to_motion_detection_event(AXEventHandler *event_handler, FILE *fp)
{
  AXEventKeyValueSet *key_value_set;
  guint subscription;

  key_value_set = ax_event_key_value_set_new();

  ax_event_key_value_set_add_key_values(key_value_set, NULL, 
  "topic0", "tns1", "RuleEngine", AX_VALUE_TYPE_STRING,
  "topic1", "tnsaxis", "VMD3", AX_VALUE_TYPE_STRING,	
  "active", NULL, NULL, AX_VALUE_TYPE_BOOL, NULL);

  ax_event_handler_subscribe(event_handler, key_value_set,
        &subscription, (AXSubscriptionCallback)subscription_callback, fp,
        NULL);

  ax_event_key_value_set_free(key_value_set);
  return subscription;
}

int main(void)
{
  GMainLoop *main_loop;
  AXEventHandler *event_handler;
  guint subscription;

  FILE *fp;
  fp = fopen("/tmp/motion_log", "a");
  
  main_loop = g_main_loop_new(NULL, FALSE);

  event_handler = ax_event_handler_new();

  subscription = subscribe_to_motion_detection_event(event_handler, fp); 

  syslog(LOG_INFO, "Subscription completed. Entering the main loop...");

  g_main_loop_run(main_loop);

  ax_event_handler_unsubscribe(event_handler, subscription, NULL);

  ax_event_handler_free(event_handler);

  fclose(fp);

  return 0;
}

