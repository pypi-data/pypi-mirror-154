"use strict";
(self["webpackChunkjupyterlab_variableinspector"] = self["webpackChunkjupyterlab_variableinspector"] || []).push([["lib_index_js"],{

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "DummyHandler": () => (/* binding */ DummyHandler),
/* harmony export */   "VariableInspectionHandler": () => (/* binding */ VariableInspectionHandler)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/datagrid */ "webpack/sharing/consume/default/@lumino/datagrid/@lumino/datagrid");
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__);


/**
 * An object that handles code inspection.
 */
class VariableInspectionHandler {
    constructor(options) {
        this._disposed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._inspected = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._isDisposed = false;
        /*
         * Handle query response. Emit new signal containing the IVariableInspector.IInspectorUpdate object.
         * (TODO: query resp. could be forwarded to panel directly)
         */
        this._handleQueryResponse = (response) => {
            const msgType = response.header.msg_type;
            switch (msgType) {
                case 'execute_result': {
                    const payload = response.content;
                    let content = payload.data['text/plain'];
                    if (content.slice(0, 1) === "'" || content.slice(0, 1) === '"') {
                        content = content.slice(1, -1);
                        content = content.replace(/\\"/g, '"').replace(/\\'/g, "'");
                    }
                    const update = JSON.parse(content);
                    const title = {
                        contextName: '',
                        kernelName: this._connector.kernelName || '',
                    };
                    this._inspected.emit({ title: title, payload: update });
                    break;
                }
                case 'display_data': {
                    const payloadDisplay = response.content;
                    let contentDisplay = payloadDisplay.data['text/plain'];
                    if (contentDisplay.slice(0, 1) === "'" ||
                        contentDisplay.slice(0, 1) === '"') {
                        contentDisplay = contentDisplay.slice(1, -1);
                        contentDisplay = contentDisplay
                            .replace(/\\"/g, '"')
                            .replace(/\\'/g, "'");
                    }
                    const updateDisplay = JSON.parse(contentDisplay);
                    const titleDisplay = {
                        contextName: '',
                        kernelName: this._connector.kernelName || '',
                    };
                    this._inspected.emit({ title: titleDisplay, payload: updateDisplay });
                    break;
                }
                default:
                    break;
            }
        };
        /*
         * Invokes a inspection if the signal emitted from specified session is an 'execute_input' msg.
         */
        this._queryCall = (sess, msg) => {
            const msgType = msg.header.msg_type;
            switch (msgType) {
                case 'execute_input': {
                    const code = msg.content.code;
                    if (!(code === this._queryCommand) &&
                        !(code === this._matrixQueryCommand) &&
                        !code.startsWith(this._widgetQueryCommand)) {
                        this.performInspection();
                    }
                    break;
                }
                default:
                    break;
            }
        };
        this._id = options.id;
        this._connector = options.connector;
        this._rendermime = options.rendermime;
        this._queryCommand = options.queryCommand;
        this._matrixQueryCommand = options.matrixQueryCommand;
        this._widgetQueryCommand = options.widgetQueryCommand;
        this._deleteCommand = options.deleteCommand;
        this._initScript = options.initScript;
        this._ready = this._connector.ready.then(() => {
            this._initOnKernel().then((msg) => {
                this._connector.iopubMessage.connect(this._queryCall);
                return;
            });
        });
        this._connector.kernelRestarted.connect((sender, kernelReady) => {
            const title = {
                contextName: '<b>Restarting kernel...</b> ',
            };
            this._inspected.emit({
                title: title,
                payload: [],
            });
            this._ready = kernelReady.then(() => {
                this._initOnKernel().then((msg) => {
                    this._connector.iopubMessage.connect(this._queryCall);
                    this.performInspection();
                });
            });
        });
    }
    get id() {
        return this._id;
    }
    get rendermime() {
        return this._rendermime;
    }
    /**
     * A signal emitted when the handler is disposed.
     */
    get disposed() {
        return this._disposed;
    }
    get isDisposed() {
        return this._isDisposed;
    }
    get ready() {
        return this._ready;
    }
    /**
     * A signal emitted when an inspector value is generated.
     */
    get inspected() {
        return this._inspected;
    }
    /**
     * Performs an inspection by sending an execute request with the query command to the kernel.
     */
    performInspection() {
        const content = {
            code: this._queryCommand,
            stop_on_error: false,
            store_history: false,
        };
        this._connector.fetch(content, this._handleQueryResponse);
    }
    /**
     * Performs an inspection of a Jupyter Widget
     */
    performWidgetInspection(varName) {
        const request = {
            code: this._widgetQueryCommand + '(' + varName + ')',
            stop_on_error: false,
            store_history: false,
        };
        return this._connector.execute(request);
    }
    /**
     * Performs an inspection of the specified matrix.
     */
    performMatrixInspection(varName, maxRows = 100000) {
        const request = {
            code: this._matrixQueryCommand + '(' + varName + ', ' + maxRows + ')',
            stop_on_error: false,
            store_history: false,
        };
        const con = this._connector;
        return new Promise((resolve, reject) => {
            con.fetch(request, (response) => {
                const msgType = response.header.msg_type;
                switch (msgType) {
                    case 'execute_result': {
                        const payload = response.content;
                        let content = payload.data['text/plain'];
                        content = content.replace(/^'|'$/g, '');
                        content = content.replace(/\\"/g, '"');
                        content = content.replace(/\\'/g, "\\\\'");
                        const modelOptions = JSON.parse(content);
                        const jsonModel = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_1__.JSONModel(modelOptions);
                        resolve(jsonModel);
                        break;
                    }
                    case 'error':
                        console.log(response);
                        reject("Kernel error on 'matrixQuery' call!");
                        break;
                    default:
                        break;
                }
            });
        });
    }
    /**
     * Send a kernel request to delete a variable from the global environment
     */
    performDelete(varName) {
        const content = {
            code: this._deleteCommand + "('" + varName + "')",
            stop_on_error: false,
            store_history: false,
        };
        this._connector.fetch(content, this._handleQueryResponse);
    }
    /*
     * Disposes the kernel connector.
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._disposed.emit(void 0);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
    /**
     * Initializes the kernel by running the set up script located at _initScriptPath.
     */
    _initOnKernel() {
        const content = {
            code: this._initScript,
            stop_on_error: false,
            silent: true,
        };
        return this._connector.fetch(content, () => {
            //no op
        });
    }
}
class DummyHandler {
    constructor(connector) {
        this._isDisposed = false;
        this._disposed = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._inspected = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._rendermime = null;
        this._connector = connector;
    }
    get disposed() {
        return this._disposed;
    }
    get isDisposed() {
        return this._isDisposed;
    }
    get inspected() {
        return this._inspected;
    }
    get rendermime() {
        return this._rendermime;
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        this._disposed.emit(void 0);
        _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal.clearData(this);
    }
    performInspection() {
        const title = {
            contextName: '. <b>Language currently not supported.</b> ',
            kernelName: this._connector.kernelName || '',
        };
        this._inspected.emit({
            title: title,
            payload: [],
        });
    }
    performMatrixInspection(varName, maxRows) {
        return new Promise((resolve, reject) => {
            reject('Cannot inspect matrices w/ the DummyHandler!');
        });
    }
    performWidgetInspection(varName) {
        const request = {
            code: '',
            stop_on_error: false,
            store_history: false,
        };
        return this._connector.execute(request);
    }
    performDelete(varName) {
        //noop
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _variableinspector__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./variableinspector */ "./lib/variableinspector.js");
/* harmony import */ var _kernelconnector__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./kernelconnector */ "./lib/kernelconnector.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _manager__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./manager */ "./lib/manager.js");
/* harmony import */ var _inspectorscripts__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./inspectorscripts */ "./lib/inspectorscripts.js");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);










var CommandIDs;
(function (CommandIDs) {
    CommandIDs.open = 'variableinspector:open';
})(CommandIDs || (CommandIDs = {}));
/**
 * A service providing variable introspection.
 */
const variableinspector = {
    id: 'jupyterlab_variableinspector',
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.ICommandPalette, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILayoutRestorer, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell],
    provides: _manager__WEBPACK_IMPORTED_MODULE_5__.IVariableInspectorManager,
    autoStart: true,
    activate: (app, palette, restorer, labShell) => {
        const manager = new _manager__WEBPACK_IMPORTED_MODULE_5__.VariableInspectorManager();
        const category = 'Variable Inspector';
        const command = CommandIDs.open;
        const label = 'Open Variable Inspector';
        const namespace = 'variableinspector';
        const tracker = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.WidgetTracker({ namespace });
        /**
         * Create and track a new inspector.
         */
        function newPanel() {
            const panel = new _variableinspector__WEBPACK_IMPORTED_MODULE_6__.VariableInspectorPanel();
            panel.id = 'jp-variableinspector';
            panel.title.label = 'Variable Inspector';
            panel.title.icon = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.listIcon;
            panel.title.closable = true;
            panel.disposed.connect(() => {
                if (manager.panel === panel) {
                    manager.panel = null;
                }
            });
            //Track the inspector panel
            tracker.add(panel);
            return panel;
        }
        // Enable state restoration
        restorer.restore(tracker, {
            command,
            args: () => null,
            name: () => 'variableinspector',
        });
        // Add command to palette
        app.commands.addCommand(command, {
            label,
            execute: () => {
                if (!manager.panel || manager.panel.isDisposed) {
                    manager.panel = newPanel();
                }
                if (!manager.panel.isAttached) {
                    labShell.add(manager.panel, 'main');
                }
                if (manager.source) {
                    manager.source.performInspection();
                }
                labShell.activateById(manager.panel.id);
            },
        });
        palette.addItem({ command, category });
        console.log('JupyterLab extension jupyterlab_variableinspector is activated!');
        return manager;
    },
};
/**
 * An extension that registers consoles for variable inspection.
 */
const consoles = {
    id: 'jupyterlab-variableinspector:consoles',
    requires: [_manager__WEBPACK_IMPORTED_MODULE_5__.IVariableInspectorManager, _jupyterlab_console__WEBPACK_IMPORTED_MODULE_2__.IConsoleTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell],
    autoStart: true,
    activate: (app, manager, consoles, labShell) => {
        const handlers = {};
        /**
         * Subscribes to the creation of new consoles. If a new notebook is created, build a new handler for the consoles.
         * Adds a promise for a instanced handler to the 'handlers' collection.
         */
        consoles.widgetAdded.connect((sender, consolePanel) => {
            if (manager.hasHandler(consolePanel.sessionContext.path)) {
                handlers[consolePanel.id] = new Promise((resolve, reject) => {
                    resolve(manager.getHandler(consolePanel.sessionContext.path));
                });
            }
            else {
                handlers[consolePanel.id] = new Promise((resolve, reject) => {
                    const session = consolePanel.sessionContext;
                    // Create connector and init w script if it exists for kernel type.
                    const connector = new _kernelconnector__WEBPACK_IMPORTED_MODULE_7__.KernelConnector({ session });
                    const scripts = connector.ready.then(() => {
                        return connector.kernelLanguage.then((lang) => {
                            return _inspectorscripts__WEBPACK_IMPORTED_MODULE_8__.Languages.getScript(lang);
                        });
                    });
                    scripts.then((result) => {
                        const initScript = result.initScript;
                        const queryCommand = result.queryCommand;
                        const matrixQueryCommand = result.matrixQueryCommand;
                        const widgetQueryCommand = result.widgetQueryCommand;
                        const deleteCommand = result.deleteCommand;
                        const options = {
                            queryCommand: queryCommand,
                            matrixQueryCommand: matrixQueryCommand,
                            widgetQueryCommand,
                            deleteCommand: deleteCommand,
                            connector: connector,
                            initScript: initScript,
                            id: session.path,
                        };
                        const handler = new _handler__WEBPACK_IMPORTED_MODULE_9__.VariableInspectionHandler(options);
                        manager.addHandler(handler);
                        consolePanel.disposed.connect(() => {
                            delete handlers[consolePanel.id];
                            handler.dispose();
                        });
                        handler.ready.then(() => {
                            resolve(handler);
                        });
                    });
                    //Otherwise log error message.
                    scripts.catch((result) => {
                        console.log(result);
                        const handler = new _handler__WEBPACK_IMPORTED_MODULE_9__.DummyHandler(connector);
                        consolePanel.disposed.connect(() => {
                            delete handlers[consolePanel.id];
                            handler.dispose();
                        });
                        resolve(handler);
                    });
                });
            }
        });
        /**
         * If focus window changes, checks whether new focus widget is a console.
         * In that case, retrieves the handler associated to the console after it has been
         * initialized and updates the manager with it.
         */
        labShell.currentChanged.connect((sender, args) => {
            const widget = args.newValue;
            if (!widget || !consoles.has(widget)) {
                return;
            }
            const future = handlers[widget.id];
            future.then((source) => {
                if (source) {
                    manager.source = source;
                    manager.source.performInspection();
                }
            });
        });
        app.contextMenu.addItem({
            command: CommandIDs.open,
            selector: '.jp-CodeConsole',
        });
    },
};
/**
 * An extension that registers notebooks for variable inspection.
 */
const notebooks = {
    id: 'jupyterlab-variableinspector:notebooks',
    requires: [_manager__WEBPACK_IMPORTED_MODULE_5__.IVariableInspectorManager, _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_3__.INotebookTracker, _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__.ILabShell],
    autoStart: true,
    activate: (app, manager, notebooks, labShell) => {
        const handlers = {};
        /**
         * Subscribes to the creation of new notebooks. If a new notebook is created, build a new handler for the notebook.
         * Adds a promise for a instanced handler to the 'handlers' collection.
         */
        notebooks.widgetAdded.connect((sender, nbPanel) => {
            //A promise that resolves after the initialization of the handler is done.
            handlers[nbPanel.id] = new Promise((resolve, reject) => {
                const session = nbPanel.sessionContext;
                const connector = new _kernelconnector__WEBPACK_IMPORTED_MODULE_7__.KernelConnector({ session });
                const rendermime = nbPanel.content.rendermime;
                const scripts = connector.ready.then(() => {
                    return connector.kernelLanguage.then((lang) => {
                        return _inspectorscripts__WEBPACK_IMPORTED_MODULE_8__.Languages.getScript(lang);
                    });
                });
                scripts.then((result) => {
                    const initScript = result.initScript;
                    const queryCommand = result.queryCommand;
                    const matrixQueryCommand = result.matrixQueryCommand;
                    const widgetQueryCommand = result.widgetQueryCommand;
                    const deleteCommand = result.deleteCommand;
                    const options = {
                        queryCommand: queryCommand,
                        matrixQueryCommand: matrixQueryCommand,
                        widgetQueryCommand,
                        deleteCommand: deleteCommand,
                        connector: connector,
                        rendermime,
                        initScript: initScript,
                        id: session.path,
                    };
                    const handler = new _handler__WEBPACK_IMPORTED_MODULE_9__.VariableInspectionHandler(options);
                    manager.addHandler(handler);
                    nbPanel.disposed.connect(() => {
                        delete handlers[nbPanel.id];
                        handler.dispose();
                    });
                    handler.ready.then(() => {
                        resolve(handler);
                    });
                });
                //Otherwise log error message.
                scripts.catch((result) => {
                    reject(result);
                });
            });
        });
        /**
         * If focus window changes, checks whether new focus widget is a notebook.
         * In that case, retrieves the handler associated to the notebook after it has been
         * initialized and updates the manager with it.
         */
        labShell.currentChanged.connect((sender, args) => {
            const widget = args.newValue;
            if (!widget || !notebooks.has(widget)) {
                return;
            }
            const future = handlers[widget.id];
            future.then((source) => {
                if (source) {
                    manager.source = source;
                    manager.source.performInspection();
                }
            });
        });
        app.contextMenu.addItem({
            command: CommandIDs.open,
            selector: '.jp-Notebook',
        });
    },
};
/**
 * Export the plugins as default.
 */
const plugins = [
    variableinspector,
    consoles,
    notebooks,
];
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugins);


/***/ }),

/***/ "./lib/inspectorscripts.js":
/*!*********************************!*\
  !*** ./lib/inspectorscripts.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "Languages": () => (/* binding */ Languages)
/* harmony export */ });
class Languages {
    static getScript(lang) {
        return new Promise((resolve, reject) => {
            if (lang in Languages.scripts) {
                resolve(Languages.scripts[lang]);
            }
            else {
                reject('Language ' + lang + ' not supported yet!');
            }
        });
    }
}
/**
 * Init and query script for supported languages.
 */
Languages.py_script = `import json
import sys
from IPython import get_ipython
from IPython.core.magics.namespace import NamespaceMagics


_jupyterlab_variableinspector_nms = NamespaceMagics()
_jupyterlab_variableinspector_Jupyter = get_ipython()
_jupyterlab_variableinspector_nms.shell = _jupyterlab_variableinspector_Jupyter.kernel.shell

__np = None
__pd = None
__pyspark = None
__tf = None
__K = None
__torch = None
__ipywidgets = None


def _check_imported():
    global __np, __pd, __pyspark, __tf, __K, __torch, __ipywidgets

    if 'numpy' in sys.modules:
        # don't really need the try
        import numpy as __np

    if 'pandas' in sys.modules:
        import pandas as __pd

    if 'pyspark' in sys.modules:
        import pyspark as __pyspark

    if 'tensorflow' in sys.modules or 'keras' in sys.modules:
        import tensorflow as __tf

        try:
            import keras.backend as __K
        except ImportError:
            try:
                import tensorflow.keras.backend as __K
            except ImportError:
                __K = None

    if 'torch' in sys.modules:
        import torch as __torch

    if 'ipywidgets' in sys.modules:
        import ipywidgets as __ipywidgets


def _jupyterlab_variableinspector_getsizeof(x):
    if type(x).__name__ in ['ndarray', 'Series']:
        return x.nbytes
    elif __pyspark and isinstance(x, __pyspark.sql.DataFrame):
        return "?"
    elif __tf and isinstance(x, __tf.Variable):
        return "?"
    elif __torch and isinstance(x, __torch.Tensor):
        return x.element_size() * x.nelement()
    elif __pd and type(x).__name__ == 'DataFrame':
        return x.memory_usage().sum()
    else:
        return sys.getsizeof(x)


def _jupyterlab_variableinspector_getshapeof(x):
    if __pd and isinstance(x, __pd.DataFrame):
        return "%d rows x %d cols" % x.shape
    if __pd and isinstance(x, __pd.Series):
        return "%d rows" % x.shape
    if __np and isinstance(x, __np.ndarray):
        shape = " x ".join([str(i) for i in x.shape])
        return "%s" % shape
    if __pyspark and isinstance(x, __pyspark.sql.DataFrame):
        return "? rows x %d cols" % len(x.columns)
    if __tf and isinstance(x, __tf.Variable):
        shape = " x ".join([str(int(i)) for i in x.shape])
        return "%s" % shape
    if __tf and isinstance(x, __tf.Tensor):
        shape = " x ".join([str(int(i)) for i in x.shape])
        return "%s" % shape
    if __torch and isinstance(x, __torch.Tensor):
        shape = " x ".join([str(int(i)) for i in x.shape])
        return "%s" % shape
    if isinstance(x, list):
        return "%s" % len(x)
    if isinstance(x, dict):
        return "%s keys" % len(x)
    return ''


def _jupyterlab_variableinspector_getcontentof(x):
    # returns content in a friendly way for python variables
    # pandas and numpy
    if __pd and isinstance(x, __pd.DataFrame):
        colnames = ', '.join(x.columns.map(str))
        content = "Columns: %s" % colnames
    elif __pd and isinstance(x, __pd.Series):
        content = str(x.values).replace(" ", ", ")[1:-1]
        content = content.replace("\\n", "")
    elif __np and isinstance(x, __np.ndarray):
        content = x.__repr__()
    elif __torch and isinstance(x, __torch.Tensor):
        if x.nelement() < 1048576:
            content = x.__repr__()
        else:
            content = 'too big'
    else:
        content = str(x)

    if len(content) > 50:
        return content[:50] + " ..."
    else:
        return content


def _jupyterlab_variableinspector_is_matrix(x):
    # True if type(x).__name__ in ["DataFrame", "ndarray", "Series"] else False
    if __pd and isinstance(x, __pd.DataFrame):
        return True
    if __pd and isinstance(x, __pd.Series):
        return True
    if __np and isinstance(x, __np.ndarray) and len(x.shape) <= 2:
        return True
    if __pyspark and isinstance(x, __pyspark.sql.DataFrame):
        return True
    if __tf and isinstance(x, __tf.Variable) and len(x.shape) <= 2:
        return True
    if __tf and isinstance(x, __tf.Tensor) and len(x.shape) <= 2:
        return True
    if __torch and isinstance(x, __torch.Tensor) and len(x.shape) <= 2:
        return True
    if isinstance(x, list):
        return True
    return False


def _jupyterlab_variableinspector_is_widget(x):
    return __ipywidgets and issubclass(x, __ipywidgets.DOMWidget)


def _jupyterlab_variableinspector_dict_list():
    _check_imported()
    def keep_cond(v):
        try:
            obj = eval(v)
            if isinstance(obj, (str, list, dict)):
                return True
            if __tf and isinstance(obj, __tf.Variable):
                return True
            if __torch and isinstance(obj, __torch.Tensor):
                return True
            if __pd and __pd is not None and (
                isinstance(obj, __pd.core.frame.DataFrame)
                or isinstance(obj, __pd.core.series.Series)):
                return True
            if v in ['__np', '__pd', '__pyspark', '__tf', '__K', '__torch', '__ipywidgets']:
                return obj is not None
            if str(obj)[0] == "<":
                return False
            if str(obj).startswith("_Feature"):
                # removes tf/keras objects
                return False
            return True
        except:
            return False
    values = _jupyterlab_variableinspector_nms.who_ls()
    if 'jlvi_brief' in values:
        vardic = [
            {
                'varName': _v,
                'varType': type(eval(_v)).__name__, 
                'varSize': '0', 
                'varShape': str(_jupyterlab_variableinspector_getshapeof(eval(_v))), 
                'varContent': '', 
                'isMatrix': False,
                'isWidget': _jupyterlab_variableinspector_is_widget(type(eval(_v)))
            }
            for _v in values if keep_cond(_v)
        ]
    else:
        vardic = [
            {
                'varName': _v,
                'varType': type(eval(_v)).__name__, 
                'varSize': '0', 
                'varShape': str(_jupyterlab_variableinspector_getshapeof(eval(_v))), 
                'varContent': str(_jupyterlab_variableinspector_getcontentof(eval(_v))), 
                'isMatrix': False,
                'isWidget': _jupyterlab_variableinspector_is_widget(type(eval(_v)))
            }
            for _v in values if keep_cond(_v)
        ]
    return json.dumps(vardic, ensure_ascii=False)


def _jupyterlab_variableinspector_getmatrixcontent(x, max_rows=10000):
    # to do: add something to handle this in the future
    threshold = max_rows

    if __pd and __pyspark and isinstance(x, __pyspark.sql.DataFrame):
        df = x.limit(threshold).toPandas()
        return _jupyterlab_variableinspector_getmatrixcontent(df.copy())
    elif __np and __pd and type(x).__name__ == "DataFrame":
        if threshold is not None:
            x = x.head(threshold)
        x.columns = x.columns.map(str)
        return x.to_json(orient="table", default_handler=_jupyterlab_variableinspector_default, force_ascii=False)
    elif __np and __pd and type(x).__name__ == "Series":
        if threshold is not None:
            x = x.head(threshold)
        return x.to_json(orient="table", default_handler=_jupyterlab_variableinspector_default, force_ascii=False)
    elif __np and __pd and type(x).__name__ == "ndarray":
        df = __pd.DataFrame(x)
        return _jupyterlab_variableinspector_getmatrixcontent(df)
    elif __tf and (isinstance(x, __tf.Variable) or isinstance(x, __tf.Tensor)):
        df = __K.get_value(x)
        return _jupyterlab_variableinspector_getmatrixcontent(df)
    elif __torch and isinstance(x, __torch.Tensor):
        df = x.cpu().numpy()
        return _jupyterlab_variableinspector_getmatrixcontent(df)
    elif isinstance(x, list):
        s = __pd.Series(x)
        return _jupyterlab_variableinspector_getmatrixcontent(s)


def _jupyterlab_variableinspector_displaywidget(widget):
    display(widget)


def _jupyterlab_variableinspector_default(o):
    if isinstance(o, __np.number): return int(o)  
    raise TypeError


def _jupyterlab_variableinspector_deletevariable(x):
    exec("del %s" % x, globals())
`;
Languages.r_script = `library(repr)

  .Last.value = 'wtf'
  
  .ls.objects = function (pos = 1, pattern, order.by, decreasing = FALSE, head = FALSE, 
      n = 5) 
  {
      napply <- function(names, fn) sapply(names, function(x) fn(get(x, 
          pos = pos)))
      names <- ls(pos = pos, pattern = pattern)
      
      if (class(base::.Last.value) != 'json') .Last.value <<- base::.Last.value
      names = c('.Last.value',names)
  
      if (length(names) == 0) {
          return(jsonlite::toJSON(data.frame()))
      }
      obj.class <- napply(names, function(x) paste(as.character(class(x)),collapse=rawToChar(as.raw(c(92,110)))))
      obj.mode <- napply(names, mode)
      obj.type <- ifelse(is.na(obj.class), obj.mode, obj.class)
      
      obj.dim <- t(napply(names, function(x) as.numeric(dim(x))[1:2]))
      has_no_dim <- is.na(obj.dim)[1:length(names)]                        
      obj.dim[has_no_dim, 1] <- napply(names, length)[has_no_dim]
      
      obj.size = rep(0,length(names))
      
      wtf = napply(names,function(x) {'patchwork' %in% class(x)})
      obj.content = rep("NA",length(names))
      if (!'jlvi_brief' %in% names) {
          obj.content[!wtf] <- napply(names[!wtf], function(x) {a=capture.output(str(x,max.level=1,list.len=4)); b=lapply(a[1:min(length(a),5)], function(x) {paste(substring(x, 1, 50), ifelse(nchar(x) > 50, "...", ""))}); paste(b,collapse=rawToChar(as.raw(c(92,110))))})
      }
          
      is_function <- (obj.type == "function")
      if (!'jlvi_brief' %in% names) {
        obj.content[is_function] <- napply(names[is_function], function(x) paste(strsplit(repr_text(x),")")[[1]][1],")",sep=""))
      }
      obj.content <- unlist(obj.content, use.names = FALSE)
      
      out <- data.frame(obj.type, obj.size, obj.dim)
      names(out) <- c("varType", "varSize", "Rows", "Columns")
      out$varShape <- paste(out$Rows, " x ", out$Columns)
      out$varContent <- obj.content
      out$isMatrix <- FALSE
      out$varName <- row.names(out)
      out <- out[, !(names(out) %in% c("Rows", "Columns"))]
      rownames(out) <- NULL
      print(out)
      if (!missing(order.by)) 
          out <- out[order(out[[order.by]], decreasing = decreasing), 
              ]
      if (head) 
          out <- head(out, n)
      jsonlite::toJSON(out)
  }
  
  .deleteVariable <- function(x) {
      remove(list=c(x), envir=.GlobalEnv)
  }
      `;
Languages.scripts = {
    python3: {
        initScript: Languages.py_script,
        queryCommand: '_jupyterlab_variableinspector_dict_list()',
        matrixQueryCommand: '_jupyterlab_variableinspector_getmatrixcontent',
        widgetQueryCommand: '_jupyterlab_variableinspector_displaywidget',
        deleteCommand: '_jupyterlab_variableinspector_deletevariable',
    },
    python2: {
        initScript: Languages.py_script,
        queryCommand: '_jupyterlab_variableinspector_dict_list()',
        matrixQueryCommand: '_jupyterlab_variableinspector_getmatrixcontent',
        widgetQueryCommand: '_jupyterlab_variableinspector_displaywidget',
        deleteCommand: '_jupyterlab_variableinspector_deletevariable',
    },
    python: {
        initScript: Languages.py_script,
        queryCommand: '_jupyterlab_variableinspector_dict_list()',
        matrixQueryCommand: '_jupyterlab_variableinspector_getmatrixcontent',
        widgetQueryCommand: '_jupyterlab_variableinspector_displaywidget',
        deleteCommand: '_jupyterlab_variableinspector_deletevariable',
    },
    R: {
        initScript: Languages.r_script,
        queryCommand: '.ls.objects()',
        matrixQueryCommand: '.ls.objects',
        widgetQueryCommand: 'TODO',
        deleteCommand: '.deleteVariable',
    },
    scala: {
        initScript: '_root_.almond.api.JupyterAPIHolder.value.VariableInspector.init()',
        queryCommand: '_root_.almond.api.JupyterAPIHolder.value.VariableInspector.dictList()',
        matrixQueryCommand: '',
        widgetQueryCommand: '',
        deleteCommand: '',
    },
};


/***/ }),

/***/ "./lib/kernelconnector.js":
/*!********************************!*\
  !*** ./lib/kernelconnector.js ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelConnector": () => (/* binding */ KernelConnector)
/* harmony export */ });
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_0__);

/**
 * Connector class that handles execute request to a kernel
 */
class KernelConnector {
    constructor(options) {
        this._kernelRestarted = new _lumino_signaling__WEBPACK_IMPORTED_MODULE_0__.Signal(this);
        this._session = options.session;
        this._session.statusChanged.connect((sender, newStatus) => {
            switch (newStatus) {
                case 'restarting':
                case 'autorestarting':
                    this._kernelRestarted.emit(this._session.ready);
                    break;
                default:
                    break;
            }
        });
    }
    get kernelRestarted() {
        return this._kernelRestarted;
    }
    get kernelLanguage() {
        return this._session.session.kernel.info.then((infoReply) => {
            return infoReply.language_info.name;
        });
    }
    get kernelName() {
        return this._session.kernelDisplayName;
    }
    /**
     *  A Promise that is fulfilled when the session associated w/ the connector is ready.
     */
    get ready() {
        return this._session.ready;
    }
    /**
     *  A signal emitted for iopub messages of the kernel associated with the kernel.
     */
    get iopubMessage() {
        return this._session.iopubMessage;
    }
    /**
     * Executes the given request on the kernel associated with the connector.
     * @param content: IExecuteRequestMsg to forward to the kernel.
     * @param ioCallback: Callable to forward IOPub messages of the kernel to.
     * @returns Promise<KernelMessage.IExecuteReplyMsg>
     */
    fetch(content, ioCallback) {
        const kernel = this._session.session.kernel;
        if (!kernel) {
            return Promise.reject(new Error('Require kernel to perform variable inspection!'));
        }
        const future = kernel.requestExecute(content);
        future.onIOPub = (msg) => {
            ioCallback(msg);
        };
        return future.done;
    }
    execute(content) {
        return this._session.session.kernel.requestExecute(content);
    }
}


/***/ }),

/***/ "./lib/manager.js":
/*!************************!*\
  !*** ./lib/manager.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IVariableInspectorManager": () => (/* binding */ IVariableInspectorManager),
/* harmony export */   "VariableInspectorManager": () => (/* binding */ VariableInspectorManager)
/* harmony export */ });
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__);

const IVariableInspectorManager = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_0__.Token('jupyterlab_extension/variableinspector:IVariableInspectorManager');
/**
 * A class that manages variable inspector widget instances and offers persistent
 * `IVariableInspector` instance that other plugins can communicate with.
 */
class VariableInspectorManager {
    constructor() {
        this._source = null;
        this._panel = null;
        this._handlers = {};
    }
    hasHandler(id) {
        if (this._handlers[id]) {
            return true;
        }
        else {
            return false;
        }
    }
    getHandler(id) {
        return this._handlers[id];
    }
    addHandler(handler) {
        this._handlers[handler.id] = handler;
    }
    /**
     * The current inspector panel.
     */
    get panel() {
        return this._panel;
    }
    set panel(panel) {
        if (this.panel === panel) {
            return;
        }
        this._panel = panel;
        if (panel && !panel.source) {
            panel.source = this._source;
        }
    }
    /**
     * The source of events the inspector panel listens for.
     */
    get source() {
        return this._source;
    }
    set source(source) {
        if (this._source === source) {
            return;
        }
        // remove subscriptions
        if (this._source) {
            this._source.disposed.disconnect(this._onSourceDisposed, this);
        }
        this._source = source;
        if (this._panel && !this._panel.isDisposed) {
            this._panel.source = this._source;
        }
        // Subscribe to new source
        if (this._source) {
            this._source.disposed.connect(this._onSourceDisposed, this);
        }
    }
    _onSourceDisposed() {
        this._source = null;
    }
}


/***/ }),

/***/ "./lib/variableinspector.js":
/*!**********************************!*\
  !*** ./lib/variableinspector.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "IVariableInspector": () => (/* binding */ IVariableInspector),
/* harmony export */   "VariableInspectorPanel": () => (/* binding */ VariableInspectorPanel)
/* harmony export */ });
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/datagrid */ "webpack/sharing/consume/default/@lumino/datagrid/@lumino/datagrid");
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_datagrid__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");






const TITLE_CLASS = 'jp-VarInspector-title';
const PANEL_CLASS = 'jp-VarInspector';
const TABLE_CLASS = 'jp-VarInspector-table';
const TABLE_BODY_CLASS = 'jp-VarInspector-content';
/**
 * The inspector panel token.
 */
const IVariableInspector = new _lumino_coreutils__WEBPACK_IMPORTED_MODULE_1__.Token('jupyterlab_extension/variableinspector:IVariableInspector');
/**
 * A panel that renders the variables
 */
class VariableInspectorPanel extends _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget {
    constructor() {
        super();
        this._source = null;
        this.addClass(PANEL_CLASS);
        this._title = Private.createTitle();
        this._title.className = TITLE_CLASS;
        this._table = Private.createTable();
        this._table.className = TABLE_CLASS;
        this.node.appendChild(this._title);
        this.node.appendChild(this._table);
    }
    get source() {
        return this._source;
    }
    set source(source) {
        if (this._source === source) {
            // this._source.performInspection();
            return;
        }
        //Remove old subscriptions
        if (this._source) {
            this._source.inspected.disconnect(this.onInspectorUpdate, this);
            this._source.disposed.disconnect(this.onSourceDisposed, this);
        }
        this._source = source;
        //Subscribe to new object
        if (this._source) {
            this._source.inspected.connect(this.onInspectorUpdate, this);
            this._source.disposed.connect(this.onSourceDisposed, this);
            this._source.performInspection();
        }
    }
    /**
     * Dispose resources
     */
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this.source = null;
        super.dispose();
    }
    onInspectorUpdate(sender, allArgs) {
        if (!this.isAttached) {
            return;
        }
        const title = allArgs.title;
        const args = allArgs.payload;
        if (title.contextName) {
            this._title.innerHTML = title.contextName;
        }
        else {
            this._title.innerHTML =
                "    Inspecting '" + title.kernelName + "' " + title.contextName;
        }
        //Render new variable state
        let row;
        this._table.deleteTFoot();
        this._table.createTFoot();
        this._table.tFoot.className = TABLE_BODY_CLASS;
        for (let index = 0; index < args.length; index++) {
            const item = args[index];
            console.log(item);
            const name = item.varName;
            const varType = item.varType;
            row = this._table.tFoot.insertRow();
            // Add delete icon and onclick event
            let cell = row.insertCell(0);
            cell.title = 'Delete Variable';
            cell.className = 'jp-VarInspector-deleteButton';
            const ico = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.closeIcon.element();
            ico.onclick = (ev) => {
                this.source.performDelete(name);
            };
            cell.append(ico);
            // Add onclick event for inspection
            cell = row.insertCell(1);
            if (item.isMatrix) {
                cell.title = 'View Contents';
                cell.className = 'jp-VarInspector-inspectButton';
                const ico = _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_4__.searchIcon.element();
                ico.onclick = (ev) => {
                    console.log('Click on ' + name);
                    this._source
                        .performMatrixInspection(name)
                        .then((model) => {
                        this._showMatrix(model, name, varType);
                    });
                };
                cell.append(ico);
            }
            else {
                cell.innerHTML = '';
            }
            // cell = row.insertCell(2);
            cell.className = 'jp-VarInspector-varName';
            cell.innerHTML = name;
            // Add remaining cells
            cell = row.insertCell(2);
            cell.innerHTML = varType.replace(/\\n/g, "</br>");
            ;
            // cell = row.insertCell(4);
            // cell.innerHTML = item.varSize;
            cell = row.insertCell(3);
            cell.innerHTML = item.varShape;
            cell = row.insertCell(4);
            const rendermime = this._source.rendermime;
            if (item.isWidget && rendermime) {
                const model = new _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.OutputAreaModel({ trusted: true });
                const output = new _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_0__.SimplifiedOutputArea({ model, rendermime });
                output.future = this._source.performWidgetInspection(item.varName);
                _lumino_widgets__WEBPACK_IMPORTED_MODULE_2__.Widget.attach(output, cell);
            }
            else {
                cell.innerHTML = Private.escapeHtml(item.varContent).replace(/\\n/g, '</br>');
            }
        }
    }
    /**
     * Handle source disposed signals.
     */
    onSourceDisposed(sender, args) {
        this.source = null;
    }
    _showMatrix(dataModel, name, varType) {
        const datagrid = new _lumino_datagrid__WEBPACK_IMPORTED_MODULE_3__.DataGrid({
            defaultSizes: {
                rowHeight: 32,
                columnWidth: 128,
                rowHeaderWidth: 64,
                columnHeaderHeight: 32,
            },
        });
        datagrid.dataModel = dataModel;
        datagrid.title.label = varType + ': ' + name;
        datagrid.title.closable = true;
        const lout = this.parent.layout;
        lout.addWidget(datagrid, { mode: 'split-right' });
        //todo activate/focus matrix widget
    }
}
var Private;
(function (Private) {
    const entityMap = new Map(Object.entries({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
        '/': '&#x2F;',
    }));
    function escapeHtml(source) {
        return String(source).replace(/[&<>"'/]/g, (s) => entityMap.get(s));
    }
    Private.escapeHtml = escapeHtml;
    function createTable() {
        const table = document.createElement('table');
        table.createTHead();
        const hrow = table.tHead.insertRow(0);
        const cell1 = hrow.insertCell(0);
        cell1.innerHTML = '';
        // const cell2 = hrow.insertCell(1);
        // cell2.innerHTML = '';
        const cell3 = hrow.insertCell(1);
        cell3.innerHTML = 'Name';
        const cell4 = hrow.insertCell(2);
        cell4.innerHTML = 'Type';
        // const cell5 = hrow.insertCell(4);
        // cell5.innerHTML = 'Size';
        const cell6 = hrow.insertCell(3);
        cell6.innerHTML = 'Shape';
        const cell7 = hrow.insertCell(4);
        cell7.innerHTML = 'Content';
        return table;
    }
    Private.createTable = createTable;
    function createTitle(header = '') {
        const title = document.createElement('p');
        title.innerHTML = header;
        return title;
    }
    Private.createTitle = createTitle;
})(Private || (Private = {}));


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/base.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/base.css ***!
  \**************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
// Imports


var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
// Module
___CSS_LOADER_EXPORT___.push([module.id, "/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n", "",{"version":3,"sources":["webpack://./style/base.css"],"names":[],"mappings":"AAAA;;;;CAIC","sourcesContent":["/*\n    See the JupyterLab Developer Guide for useful CSS Patterns:\n\n    https://jupyterlab.readthedocs.io/en/stable/developer/css.html\n*/\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./style/index.css":
/*!***************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./style/index.css ***!
  \***************************************************************/
/***/ ((module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/cssWithMappingToString.js */ "./node_modules/css-loader/dist/runtime/cssWithMappingToString.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
/* harmony import */ var _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! -!../node_modules/css-loader/dist/cjs.js!./base.css */ "./node_modules/css-loader/dist/cjs.js!./style/base.css");
// Imports



var ___CSS_LOADER_EXPORT___ = _node_modules_css_loader_dist_runtime_api_js__WEBPACK_IMPORTED_MODULE_1___default()((_node_modules_css_loader_dist_runtime_cssWithMappingToString_js__WEBPACK_IMPORTED_MODULE_0___default()));
___CSS_LOADER_EXPORT___.i(_node_modules_css_loader_dist_cjs_js_base_css__WEBPACK_IMPORTED_MODULE_2__["default"]);
// Module
___CSS_LOADER_EXPORT___.push([module.id, "\n.jp-VarInspector {\n    flex-direction: column;\n    overflow: auto;\n    font-size: var(--jp-ui-font-size1);\n  }\n  \n  .jp-VarInspector-table {\n    border-collapse: collapse;\n    margin: auto;\n    width: 100%;\n    color: var(--jp-content-font-color1);\n  }\n  \n  .jp-VarInspector-table td,\n  .jp-VarInspector-table thead {\n    border: 1px solid;\n    border-color: var(--jp-layout-color2);\n    padding: 8px;\n  }\n  \n  .jp-VarInspector-table tr:nth-child(even) {\n    background-color: var(--jp-layout-color1);\n  }\n  \n  .jp-VarInspector-content tr:hover {\n    background-color: var(--jp-layout-color2);\n  }\n  \n  .jp-VarInspector-table thead {\n    font-size: var(--jp-ui-font-size0);\n    text-align: center;\n    background-color: var(--jp-layout-color2);\n    color: var(--jp-ui-font-color1);\n    font-weight: 600;\n    letter-spacing: 1px;\n    text-transform: uppercase;\n  }\n  \n  .jp-VarInspector-title {\n    font-size: var(--jp-ui-font-size1);\n    color: var(--jp-content-font-color1);\n    text-align: left;\n    padding-left: 10px;\n  }\n  \n  .jp-VarInspector-deleteButton {\n    text-align: center;\n    width: 1em;\n  }\n\n  .jp-VarInspector-deleteButton:hover {\n    text-shadow: 0 0 0 red;\n    background-color: var(--jp-layout-color3);\n  }\n\n  .jp-VarInspector-inspectButton {\n    text-align: center;\n    width: 1em;\n  }\n    \n    \n  .jp-VarInspector-varName {\n    font-weight: 600;\n  }\n\n", "",{"version":3,"sources":["webpack://./style/index.css"],"names":[],"mappings":";AAGA;IACI,sBAAsB;IACtB,cAAc;IACd,kCAAkC;EACpC;;EAEA;IACE,yBAAyB;IACzB,YAAY;IACZ,WAAW;IACX,oCAAoC;EACtC;;EAEA;;IAEE,iBAAiB;IACjB,qCAAqC;IACrC,YAAY;EACd;;EAEA;IACE,yCAAyC;EAC3C;;EAEA;IACE,yCAAyC;EAC3C;;EAEA;IACE,kCAAkC;IAClC,kBAAkB;IAClB,yCAAyC;IACzC,+BAA+B;IAC/B,gBAAgB;IAChB,mBAAmB;IACnB,yBAAyB;EAC3B;;EAEA;IACE,kCAAkC;IAClC,oCAAoC;IACpC,gBAAgB;IAChB,kBAAkB;EACpB;;EAEA;IACE,kBAAkB;IAClB,UAAU;EACZ;;EAEA;IACE,sBAAsB;IACtB,yCAAyC;EAC3C;;EAEA;IACE,kBAAkB;IAClB,UAAU;EACZ;;;EAGA;IACE,gBAAgB;EAClB","sourcesContent":["\n@import url('base.css');\n\n.jp-VarInspector {\n    flex-direction: column;\n    overflow: auto;\n    font-size: var(--jp-ui-font-size1);\n  }\n  \n  .jp-VarInspector-table {\n    border-collapse: collapse;\n    margin: auto;\n    width: 100%;\n    color: var(--jp-content-font-color1);\n  }\n  \n  .jp-VarInspector-table td,\n  .jp-VarInspector-table thead {\n    border: 1px solid;\n    border-color: var(--jp-layout-color2);\n    padding: 8px;\n  }\n  \n  .jp-VarInspector-table tr:nth-child(even) {\n    background-color: var(--jp-layout-color1);\n  }\n  \n  .jp-VarInspector-content tr:hover {\n    background-color: var(--jp-layout-color2);\n  }\n  \n  .jp-VarInspector-table thead {\n    font-size: var(--jp-ui-font-size0);\n    text-align: center;\n    background-color: var(--jp-layout-color2);\n    color: var(--jp-ui-font-color1);\n    font-weight: 600;\n    letter-spacing: 1px;\n    text-transform: uppercase;\n  }\n  \n  .jp-VarInspector-title {\n    font-size: var(--jp-ui-font-size1);\n    color: var(--jp-content-font-color1);\n    text-align: left;\n    padding-left: 10px;\n  }\n  \n  .jp-VarInspector-deleteButton {\n    text-align: center;\n    width: 1em;\n  }\n\n  .jp-VarInspector-deleteButton:hover {\n    text-shadow: 0 0 0 red;\n    background-color: var(--jp-layout-color3);\n  }\n\n  .jp-VarInspector-inspectButton {\n    text-align: center;\n    width: 1em;\n  }\n    \n    \n  .jp-VarInspector-varName {\n    font-weight: 600;\n  }\n\n"],"sourceRoot":""}]);
// Exports
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (___CSS_LOADER_EXPORT___);


/***/ }),

/***/ "./style/index.css":
/*!*************************!*\
  !*** ./style/index.css ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
/* harmony import */ var _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./index.css */ "./node_modules/css-loader/dist/cjs.js!./style/index.css");

            

var options = {};

options.insert = "head";
options.singleton = false;

var update = _node_modules_style_loader_dist_runtime_injectStylesIntoStyleTag_js__WEBPACK_IMPORTED_MODULE_0___default()(_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"], options);



/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (_node_modules_css_loader_dist_cjs_js_index_css__WEBPACK_IMPORTED_MODULE_1__["default"].locals || {});

/***/ })

}]);
//# sourceMappingURL=lib_index_js.4b2a7d4837caf0fa7260.js.map