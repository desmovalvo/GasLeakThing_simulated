#!/usr/bin/python3

# global requirements
import time
import random
from uuid import uuid4
from datetime import datetime
from termcolor import colored
from sepy.Producer import Producer


# main
if __name__ == "__main__":

    # create an instance of the Producer
    p = Producer("ThingDescription.jsap", "SepaParameters.jpar")

    # namespaces
    wot = "http://www.arces.unibo.it/wot#"
    
    # create thing data
    thingURI = "<" + wot + str(uuid4()) + ">"
    thingName = "FakeThing"
    thingLocation = "<" + wot + "MyLocation>"

    # creating thing's property
    propertyURI = "<" + wot + str(uuid4()) + ">"
    propertyName = "GasLeak"
    propertyValueTypeURI = "<" + wot + str(uuid4()) + ">"

    # creating the thing's 'property changed' event
    eventURI = "<" + wot + str(uuid4()) + ">"
    eventName = "GasLeakEvent"

    # creating a timestamp event
    hbEventURI = "<" + wot + str(uuid4()) + ">"
    hbEventName = "GasLeak Heartbeat"
    
    # initialize the Thing
    print(colored("sensor:", "blue", attrs=["bold"]) + " init1") 
    p.produce("INIT_TD", {"thing":thingURI,
                          "thingName":thingName,
                          "thingLocation":thingLocation,
                          "discoverable":"true"})

    # add a property to the Thing
    print(colored("sensor:", "blue", attrs=["bold"]) + " init2") 
    p.produce("ADD_PROPERTY", {"thing":thingURI,
                               "propertyUUID":propertyURI,
                               "propertyUUIDName":propertyName,
                               "propertyUUIDStability":"-1",
                               "propertyUUIDWritability":"false",
                               "propertyUUIDValueType":propertyValueTypeURI,
                               "propertyUUIDValueTypeContent":"false"})

    # add a property changed event
    print(colored("sensor:", "blue", attrs=["bold"]) + " init3") 
    p.produce("ADD_PROPERTY_CHANGED_EVENT", {"thing":thingURI,
                                             "eventUUID":eventURI,
                                             "eventUUIDName":eventName})

    # bind the property to the event
    print(colored("sensor:", "blue", attrs=["bold"]) + " init4") 
    p.produce("APPEND_TARGET_PROPERTY_TO_ACTION_OR_EVENT", {"action_OR_event":eventURI,
                                                            "targetPropertyUUID":propertyURI})

    # initialise the value of the sensor to False
    gasLeakValue = False
    
    # now start an endless loop that stops only with a CTRL-C
    while True:

        # sleep for nine seconds
        time.sleep(9)

        # generate a timestamp
        timestamp = datetime.timestamp(datetime.now())
        
        # check the new value
        newValue = bool(random.getrandbits(1))
        if newValue != gasLeakValue:

            # debug
            print(colored("sensor:", "blue", attrs=["bold"]) + " updating value")
            
            # update the value in memory
            gasLeakValue = newValue

            # update the value in the context store
            newInstanceURI = "<" + wot + str(uuid4()) + ">"
            newOutputURI = "<" + wot + str(uuid4()) + ">"
            strNewValue = "true" if newValue else "false"
            p.produce("POST_NEW_EVENT_WITH_OUTPUT", {"event":eventURI,
                                                     "newInstance":newInstanceURI,
                                                     "eNewTimeStamp":timestamp,
                                                     "eNewOutput":newOutputURI,
                                                     "newValue":strNewValue})            
            
        
        # update the timestamp
        newInstanceURI = "<" + wot + str(uuid4()) + ">"
        timestamp = datetime.timestamp(datetime.now())
        p.produce("POST_NEW_EVENT_WITHOUT_OUTPUT", {"event":hbEventURI,
                                                "newInstance":newInstanceURI,
                                                "eNewTimeStamp":timestamp})
    
