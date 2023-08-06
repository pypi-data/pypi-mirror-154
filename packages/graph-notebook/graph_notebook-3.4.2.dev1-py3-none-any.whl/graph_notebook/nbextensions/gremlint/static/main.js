/*
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: Apache-2.0
 */

require(['../../../widgets/node_modules/gremlint/lib/index.js'], function(gremlint) {
    console.log('GREMLINT CHECKING')
    import { formatQuery } from 'gremlint';
    //Jupyter.CodeCell.options_default.highlight_modes['text/x-groovy'] = {reg:["/^%%gremlin/"]} ;
    Jupyter.notebook.events.one('kernel_ready.Kernel', function(){
        Jupyter.notebook.get_cells().map(function(cell) {
            if (cell.cell_type === 'code') {
                console.log("USING GREMLINT");
                console.log(cell);
                console.log("Cell type:");
                console.log(cell.cell_type);
                console.log("Value of cell:");
                console.log(cell.valueOf());
                console.log("Cell to String:");
                console.log(cell.toString());
                const source = cell.code_mirror.getValue();
                console.log("Value from CodeMirror:");
                console.log(source);
                const formattedQuery = gremlint.formatQuery(source);
                console.log("Formatted Query:");
                console.log(formattedQuery);
                cell.code_mirror.setValue(formattedQuery);
            }
        });
    });
});