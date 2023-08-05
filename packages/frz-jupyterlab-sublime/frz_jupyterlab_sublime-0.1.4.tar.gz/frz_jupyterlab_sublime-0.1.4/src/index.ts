import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { INotebookTracker } from '@jupyterlab/notebook';

import { CodeMirrorEditor } from '@jupyterlab/codemirror';

import '../style/index.css';


class JupyterLabSublime {
    private app: JupyterFrontEnd;
    private tracker: INotebookTracker;

    constructor(app: JupyterFrontEnd, tracker: INotebookTracker) {
        this.app = app;
        this.tracker = tracker;
        this.addCommands();
        this.onActiveCellChanged();
        this.tracker.activeCellChanged.connect(this.onActiveCellChanged, this);
    }

    private addCommands() {
        const { commands } = this.app;
        const tracker = this.tracker;
        function editorExec(id: string) {
            if (tracker.activeCell !== null) {
                (tracker.activeCell.editor as CodeMirrorEditor).editor.execCommand(id);
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
            let cmd = all_commands[i]
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
                    return
                }
                const cEditor = (tracker.activeCell.editor as CodeMirrorEditor)
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
                    console.log(
                        'Inogred attempt to delete subword, because some selection is part of the same subword'
                    );
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
                    return
                }
                const cEditor = (tracker.activeCell.editor as CodeMirrorEditor)
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
                    console.log(
                        'Inogred attempt to delete subword, because some selection is part of the same subword'
                    );
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

    private onActiveCellChanged(): void {
        const activeCell = this.tracker.activeCell;
        if (activeCell !== null) {
            (activeCell.editor as CodeMirrorEditor).setOption('keyMap', 'sublime');
        }
    }
}

/**
 * Initialization data for the jupyterlab_sublime extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
    id: 'jupyterlab_sublime:plugin',
    autoStart: true,
    requires: [INotebookTracker],
    activate: (app: JupyterFrontEnd, tracker: INotebookTracker) => {
        new JupyterLabSublime(app, tracker);
        console.log('JupyterLab extension jupyterlab_sublime is activated!');
    }
};

export default plugin;
