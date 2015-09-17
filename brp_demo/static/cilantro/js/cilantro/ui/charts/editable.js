define(["jquery","underscore","./dist","./axis"],function(i,e,t,s){var o=t.FieldChart.extend({template:"charts/editable-chart",toolbarAnimationTime:200,formAnimationTime:300,events:e.extend({"click .fullsize":"toggleExpanded"},t.FieldChart.prototype.events),ui:e.extend({toolbar:".btn-toolbar",fullsizeToggle:".fullsize",form:".editable",xAxis:"[name=x-Axis]",yAxis:"[name=y-Axis]",series:"[name=series]"},t.FieldChart.prototype.ui),onRender:function(){this.options.editable===!1?(this.ui.form.detach(),this.ui.toolbar.detach()):(this.xAxis=new s.FieldAxis({el:this.ui.xAxis,collection:this.collection}),this.yAxis=new s.FieldAxis({el:this.ui.yAxis,collection:this.collection}),this.series=new s.FieldAxis({el:this.ui.series,enumerableOnly:!0,collection:this.collection}),this.model&&(this.model.get("xAxis")&&this.ui.form.hide(),this.model.get("expanded")?this.expand():this.contract()))},customizeOptions:function(e){if(this.ui.status.detach(),this.ui.heading.text(e.title.text),e.title.text="",!e.series[0])return void this.ui.chart.html("<p class=no-data>Unfortunately, there is no data to graph here.</p>");this.ui.form.hide();var t=[];return e.clustered&&t.push("Clustered"),t[0]&&(this.ui.status.text(t.join(", ")).show(),this.ui.heading.append(this.$status)),this.interactive(e)&&this.enableChartEvents(),i.extend(!0,e,this.chartOptions),e.chart.renderTo=this.ui.chart[0],e},changeChart:function(i){i&&i.preventDefault();var e=this;this.collection.when(function(){var t,s,o,l;if((null===i||"undefined"==typeof i)&&(t=e.model.get("xAxis"),t&&e.xAxis.$el.val(t.toString()),s=e.model.get("yAxis"),s&&e.yAxis.$el.val(s.toString()),o=e.model.get("series"),o&&this.series.$el.val(o.toString())),t=e.xAxis.getSelected(),s=e.yAxis.getSelected(),o=e.series.getSelected(),t){var n=e.model.get("_links").distribution.href,a=[t],r="dimension="+t.id;s&&(a.push(s),r=r+"&dimension="+s.id),o&&(l=s?2:1,r=r+"&dimension="+o.id),i&&e.model&&e.model.set({xAxis:t.id,yAxis:s?s.id:null,series:o?o.id:null}),e.update(n,r,a,l)}})},disableSelected:function(e){var t=i(e.target);this.xAxis.el===e.target?(this.yAxis.$("option").prop("disabled",!1),this.series.$("option").prop("disabled",!1)):this.yAxis.el===e.target?(this.xAxis.$("option").prop("disabled",!1),this.series.$("option").prop("disabled",!1)):(this.xAxis.$("option").prop("disabled",!1),this.yAxis.$("option").prop("disabled",!1));var s=t.val();""!==s&&(this.xAxis.el===e.target?(this.yAxis.$("option[value="+s+"]").prop("disabled",!0).val(""),this.series.$("option[value="+s+"]").prop("disabled",!0).val("")):this.yAxis.el===e.target?(this.xAxis.$("option[value="+s+"]").prop("disable",!0).val(""),this.series.$("option[value="+s+"]").prop("disable",!0).val("")):(this.xAxis.$("option[value="+s+"]").prop("disable",!0).val(""),this.yAxis.$("option[value="+s+"]").prop("disable",!0).val("")))},toggleExpanded:function(){var i=this.model.get("expanded");i?this.contract():this.expand(),this.model.save({expanded:!i})},resize:function(){var i=this.ui.chart.width();this.chart&&this.chart.setSize(i,null,!1)},expand:function(){this.$fullsizeToggle.children("i").removeClass("icon-resize-small").addClass("icon-resize-full"),this.$el.addClass("expanded"),this.resize()},contract:function(){this.$fullsizeToggle.children("i").removeClass("icon-resize-full").addClass("icon-resize-small"),this.$el.removeClass("expanded"),this.resize()},hideToolbar:function(){this.ui.toolbar.fadeOut(this.toolbarAnimationTime)},showToolbar:function(){this.ui.toolbar.fadeIn(this.toolbarAnimationTime)},toggleEdit:function(){this.ui.form.is(":visible")?this.ui.form.fadeOut(this.formAnimationTime):this.ui.form.fadeIn(this.formAnimationTime)}});return{EditableFieldChart:o}});
//# sourceMappingURL=editable.js.map