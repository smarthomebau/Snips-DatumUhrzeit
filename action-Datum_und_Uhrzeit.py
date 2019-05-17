#!/usr/bin/env python3

from hermes_python.hermes import Hermes, MqttOptions
import datetime
import random
import toml


USERNAME_INTENTS = "domi"
MQTT_BROKER_ADDRESS = "localhost:1883"
MQTT_USERNAME = None
MQTT_PASSWORD = None


def user_intent(intentname):
    return USERNAME_INTENTS + ":" + intentname


def subscribe_intent_callback(hermes, intent_message):
    intentname = intent_message.intent.intent_name

    if intentname == user_intent("currentDate"):
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        day = datetime.datetime.now().day
        weekday = datetime.datetime.now().isoweekday()
        weekday_list = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        result_sentence = "Heute ist {0}, der {1}.{2}.{3} .".format(weekday_list[weekday - 1], day, month, year)
        current_session_id = intent_message.session_id
        hermes.publish_end_session(current_session_id, result_sentence)

    elif intentname == user_intent("currentTime"):
        hours = datetime.datetime.now().hour
        minutes = datetime.datetime.now().minute
        if minutes == 0:
            minutes = ""
        if hours == 1:
            result_sentence = "ein Uhr {0} .".format(minutes)
        else:
            result_sentence = "{0} Uhr {1} .".format(hours, minutes)
        first_part = ["Gerade ist es", "Es ist jetzt", "Es ist", "Die aktuelle Zeit ist"]
        result_sentence = random.choice(first_part) + " " + result_sentence
        current_session_id = intent_message.session_id
        hermes.publish_end_session(current_session_id, result_sentence)

    elif intentname == user_intent("weekNumber"):
        datetime_str = intent_message.slots.date.first().value[:-10]
        datetime_obj = datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        result_sentence = "An diesem Datum ist die Kalenderwoche {0}".format(datetime_obj.isocalendar()[1])
        current_session_id = intent_message.session_id
        hermes.publish_end_session(current_session_id, result_sentence)

    elif intentname == user_intent("dateInfo"):
        result_sentence = "Diese Funktion ist noch nicht vorhanden, wird aber bald hinzugefügt."
        datetype = intent_message.slots.datetype.first().value
        if datetype == 'weekday' or 'wochentag' in datetype:
            weekday = datetime.datetime.now().isoweekday()
            weekday_list = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
            result_sentence = "Heute haben wir {weekday}.".format(weekday=weekday_list[weekday - 1])
        elif datetype == 'year':
            year = datetime.datetime.now().year
            result_sentence = "Wir sind im Jahr {year}".format(year=year)
        elif datetype == 'weeknumber' or 'kw' in datetype:
            weeknumber = datetime.datetime.now().isocalendar()[1]
            result_sentence = "Wir haben gerade die Kalenderwoche {weeknumber}".format(weeknumber=weeknumber)
        elif datetype == 'minute':
            minutes = datetime.datetime.now().minute
            result_sentence = "Wir haben die Minute {minutes}".format(minutes=minutes)
        elif datetype == 'hour':
            hours = datetime.datetime.now().hour
            result_sentence = "Wir haben gerade die Stunde {hours}".format(hours=hours)
        current_session_id = intent_message.session_id
        hermes.publish_end_session(current_session_id, result_sentence)


if __name__ == "__main__":
    snips_config = toml.load('/etc/snips.toml')
    if 'mqtt' in snips_config['snips-common'].keys():
        MQTT_BROKER_ADDRESS = snips_config['snips-common']['mqtt']
    if 'mqtt_username' in snips_config['snips-common'].keys():
        MQTT_USERNAME = snips_config['snips-common']['mqtt_username']
    if 'mqtt_password' in snips_config['snips-common'].keys():
        MQTT_PASSWORD = snips_config['snips-common']['mqtt_password']

    mqtt_opts = MqttOptions(username=MQTT_USERNAME, password=MQTT_PASSWORD, broker_address=MQTT_BROKER_ADDRESS)
    with Hermes(mqtt_options=mqtt_opts) as h:
        h.subscribe_intents(subscribe_intent_callback).start()
