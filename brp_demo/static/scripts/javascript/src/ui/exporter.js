/* global define */

define([
    'cilantro',
    'underscore',
    ], function(c, _) {

        var ExporterDialog = c.ui.ExporterDialog.extend({

            initialize: function(){
                c.ui.ExporterDialog.prototype.initialize.call(this);
                this.listenTo(this.data.exporters, 'sync', function(){
                    var url = c.session.get('url')
                    this.data.exporters.reset([
                        {
                            href: this.data.exporters.get('csv').get('href'),
                            title: 'Patients',
                            description: '',
                            type: 'csv'
                        },
                        {
                            href: url + 'aliquots/export/',
                            title: 'Aliquots',
                            description: '',
                            type: 'aliquots'
                        }
                    ])
                })
                this.options.requestDelay = 3000;
            }
        });


        return {
            ExporterDialog: ExporterDialog
        };

    });
