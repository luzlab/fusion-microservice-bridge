#Author-FATHOM
#Description-Adds FATHOM SmartQuote capabilities to Fusion360

import adsk.core
import adsk.fusion
import traceback
import json
import tempfile
    
commandId = 'FATHOM-Microservice';
commandName = 'FATHOM Microservice';
commandDescription = 'Executes a javascript job';
cmdDef = None;
app = adsk.core.Application.get()
ui = app.userInterface   
commandDefinition = None
handlers = []
development = None;

def run(context):
    try:
        onStartupCompleted = StartupCompletedHandler()
        app.startupCompleted.add(onStartupCompleted)
        handlers.append(onStartupCompleted)

        if app.isStartupComplete:
            ui.messageBox('Fusion360 has already started up...')
            # startup is already completed, which means the MicroserviceBridge was likely started\
            # from the UI. Since the StartupCompledHandler would not get called in this circumstance
            # we have to setup the URLOpeningHandler here instead.

            onOpeningFromURL = URLOpeningHandler()
            app.openingFromURL.add(onOpeningFromURL)
            handlers.append(onOpeningFromURL)

            cmdDef = ui.commandDefinitions.itemById(commandId)

            if not cmdDef:
                raise ReferenceError('{} command not found'.format(commandId))
    except:
        if ui:
            ui.messageBox('MicroserviceBridge start failed:\n{}'.format(traceback.format_exc()))

class URLOpeningHandler(adsk.core.WebRequestEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        ui.messageBox('Running!');
        eventArgs = adsk.core.WebRequestEventArgs.cast(args)
        eventArgs.isCanceled = True
        cmdDef = ui.commandDefinitions.itemById(commandId)
        if not cmdDef:
            raise ReferenceError('{} command not found'.format(commandId))
        # data = eventArgs.privateInfo;
        data = {'Name': 'Zara', 'Age': 7}
        # with open(data, 'w') as outfile:
        #     json.dump('foobar', outfile, indent=4);

        # tempfile.gettempdir()
        ui.messageBox('ID is '+eventArgs.id);
        ui.messageBox('Temp dir is '+tempfile.gettempdir());
        

        # namedValues = adsk.core.NamedValues.create();
        # namedValues.add('params', adsk.core.ValueInput.createByString(eventArgs.privateInfo))
        # (returnValue, name, value) = namedValues.getByIndex(0);
        # ui.messageBox('privateInfo = {}'.format(value.stringValue))
        # cmdDef.execute(namedValues)
    def destroy(self):
        app.openingFromURL.remove(self)


class StartupCompletedHandler(adsk.core.ApplicationEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, args):
        try:
            onOpeningFromURL = URLOpeningHandler()
            app.openingFromURL.add(onOpeningFromURL)
            handlers.append(onOpeningFromURL)

        except:
            if ui:
                ui.messageBox('MicroserviceBridge Failed to start:\n{}'.format(traceback.format_exc()))
    def destroy(self):
        app.startupCompleted.remove(self)

def stop(context):
    try:
        for handler in handlers:
            handler.destroy()
    except:
        if ui:
            ui.messageBox('MicroserviceBridge Stop Failed: {}'.format(traceback.format_exc()))