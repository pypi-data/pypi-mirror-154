"use strict";
(self["webpackChunkjupyterlab_sublime"] = self["webpackChunkjupyterlab_sublime"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_index_css__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/index.css */ "./style/index.css");


class JupyterLabSublime {
    constructor(app, tracker) {
        this.app = app;
        this.tracker = tracker;
        this.addCommands();
        this.onActiveCellChanged();
        this.tracker.activeCellChanged.connect(this.onActiveCellChanged, this);
    }
    addCommands() {
        const { commands } = this.app;
        const tracker = this.tracker;
        function editorExec(id) {
            if (tracker.activeCell !== null) {
                tracker.activeCell.editor.editor.execCommand(id);
            }
        }
        // Manage Escape collision
        // TODO: Check if use has Escape set for command mode
        commands.addCommand('sublime:exit-editor', {
            execute: () => {
                editorExec('singleSelectionTop');
                commands.execute('notebook:enter-command-mode');
            },
            label: 'Exit Editor'
        });
        // Manage Shift-Tab collision
        commands.addCommand('sublime:indent-less-slash-tooltip', {
            execute: () => {
                if (tracker.activeCell !== null) {
                    if (!tracker.activeCell.editor.host.classList.contains('jp-mod-completer-enabled')) {
                        editorExec('indentLess');
                    }
                    else {
                        commands.execute('tooltip:launch-notebook');
                    }
                }
            },
            label: 'Indent less or tooltip'
        });
        let all_commands = ["addCursorToNextLine", "addCursorToPrevLine", "clearBookmarks", "deleteLine", "deleteToSublimeMark", "delLineLeft", "delLineRight", "downcaseAtCursor", "duplicateLine", "findAllUnder", "findIncremental", "findIncrementalReverse", "findNext", "findPrev", "findUnder", "findUnderPrevious", "fold", "foldAll", "goSubwordLeft", "goSubwordRight", "goToBracket", "insertLineAfter", "insertLineBefore", "joinLines", "nextBookmark", "prevBookmark", "replace", "scrollLineDown", "scrollLineUp", "selectBetweenBrackets", "selectBookmarks", "selectLine", "selectNextOccurrence", "selectScope", "selectToSublimeMark", "setSublimeMark", "showInCenter", "skipAndSelectNextOccurrence", "smartBackspace", "sortLines", "sortLinesInsensitive", "splitSelectionByLine", "sublimeYank", "swapLineDown", "swapLineUp", "swapWithSublimeMark", "toggleBookmark", "toggleCommentIndented", "transposeChars", "unfold", "unfoldAll", "upcaseAtCursor", "wrapLines"];
        for (let i = 0; i < all_commands.length; i++) {
            let cmd = all_commands[i];
            commands.addCommand('sublime:' + cmd, {
                execute: () => {
                    editorExec(cmd);
                },
                label: cmd,
            });
        }
        commands.addCommand('sublime:subword-backward-deletion', {
            execute: () => {
                if (tracker.activeCell == null) {
                    return;
                }
                const cEditor = tracker.activeCell.editor
                    .editor;
                const doc = cEditor.getDoc();
                const starts = doc.listSelections();
                // NOTE: This is non-trivial to deal with, results are often ugly, let's ignore this.
                if (starts.some(pos => pos.head.ch !== pos.anchor.ch)) {
                    // tslint:disable-next-line:no-console
                    console.log('Ignored attempt to delete subword!');
                    return;
                }
                // CAV: To make sure when we undo this operation, we have carets showing in
                //      their rightful positions.
                cEditor.execCommand('goSubwordLeft');
                const ends = doc.listSelections();
                doc.setSelections(starts);
                if (starts.length !== ends.length) {
                    // NOTE: Edge case where select are part of the same subword, need more thoughts on this.)
                    // tslint:disable-next-line:no-console
                    console.log('Inogred attempt to delete subword, because some selection is part of the same subword');
                    return;
                }
                cEditor.operation(() => {
                    for (let i = 0; i < starts.length; i++) {
                        doc.replaceRange('', starts[i].head, ends[i].head, '+delete');
                    }
                });
            },
            label: 'Subward backward deletion'
        });
        commands.addCommand('sublime:subword-forward-deletion', {
            execute: () => {
                if (tracker.activeCell == null) {
                    return;
                }
                const cEditor = tracker.activeCell.editor
                    .editor;
                const doc = cEditor.getDoc();
                const starts = doc.listSelections();
                // NOTE: This is non-trivial to deal with, results are often ugly, let's ignore this.
                if (starts.some(pos => pos.head.ch !== pos.anchor.ch)) {
                    // tslint:disable-next-line:no-console
                    console.log('Ignored attempt to delete subword!');
                    return;
                }
                // CAV: To make sure when we undo this operation, we have carets showing in
                //      their rightful positions.
                cEditor.execCommand('goSubwordRight');
                const ends = doc.listSelections();
                doc.setSelections(starts);
                if (starts.length !== ends.length) {
                    // NOTE: Edge case where select are part of the same subword, need more thoughts on this.)
                    // tslint:disable-next-line:no-console
                    console.log('Inogred attempt to delete subword, because some selection is part of the same subword');
                    return;
                }
                cEditor.operation(() => {
                    for (let i = 0; i < starts.length; i++) {
                        doc.replaceRange('', starts[i].head, ends[i].head, '+delete');
                    }
                });
            },
            label: 'Subward forward deletion'
        });
    }
    onActiveCellChanged() {
        const activeCell = this.tracker.activeCell;
        if (activeCell !== null) {
            activeCell.editor.setOption('keyMap', 'sublime');
        }
    }
}
/**
 * Initialization data for the jupyterlab_sublime extension.
 */
const plugin = {
    id: 'jupyterlab_sublime:plugin',
    autoStart: true,
    requires: [_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_0__.INotebookTracker],
    activate: (app, tracker) => {
        new JupyterLabSublime(app, tracker);
        console.log('JupyterLab extension jupyterlab_sublime is activated!');
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


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
___CSS_LOADER_EXPORT___.push([module.id, "\n", "",{"version":3,"sources":[],"names":[],"mappings":"","sourceRoot":""}]);
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
//# sourceMappingURL=lib_index_js.0c1f04bc5478a63deab2.js.map