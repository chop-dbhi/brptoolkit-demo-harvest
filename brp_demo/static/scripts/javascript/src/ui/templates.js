/* global define */

define([
    'cilantro',
    'tpl!../templates/results.html',
    'tpl!../templates/welcome.html'
    ], function(c) {

        var templates = [].slice.call(arguments, 1);
        c.templates.set(templates);

    });
