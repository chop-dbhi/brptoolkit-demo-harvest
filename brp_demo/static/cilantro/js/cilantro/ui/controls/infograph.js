define(["jquery","underscore","backbone","marionette","./base"],function(e,t,o,i,n){var l=function(e){return function(o){var i=o.get(e);return t.isString(i)&&(i=i.toLowerCase()),i}},r=o.Model.extend({}),s=o.Collection.extend({model:r,comparator:function(e){return-e.get("count")},sortModelsBy:function(e){var t=e.chartAt(0);"-"===t&&(e=e.slice(1)),this.models=this.sortBy(l(e)),"-"===t&&this.models.reverse(),this.trigger("sort",this)}}),a=i.ItemView.extend({className:"info-bar",template:"controls/infograph/bar",options:{total:null},ui:{bar:".bar",barLabel:".bar-label"},events:{click:"toggleSelected"},modelEvents:{"change:selected":"setSelected","change:visible":"setVisible"},initialize:function(){t.bindAll(this,"onExcludedChange"),this.listenTo(this.model.collection,"change:excluded",this.onExcludedChange)},serializeData:function(){var e=this.model.toJSON(),t=this.getPercentage();return e.width=t,e.percentage=1>t?"<1":parseInt(t),e},onRender:function(){this.setSelected(this.model,!!this.model.get("selected")),""===this.ui.barLabel.html()&&this.ui.barLabel.html("(empty)"),"null"===this.ui.barLabel.html()&&this.ui.barLabel.html("(null)")},getPercentage:function(){return this.model.get("count")/this.options.total*100},toggleSelected:function(){this.model.set("selected",!this.model.get("selected"))},onExcludedChange:function(){this.$el.toggleClass("excluded",this.model.get("excluded"))},setSelected:function(e,t){this.$el.toggleClass("selected",t),t||e.get("visible")!==!1||this.$el.removeClass("filtered").hide()},setVisible:function(e,t){t?this.$el.removeClass("filtered").show():e.get("selected")?this.$el.addClass("filtered"):this.$el.hide()}}),c=n.ControlCollectionView.extend({className:"info-bar-chart",itemView:a,itemViewOptions:function(e){return{model:e,total:this.calcTotal()}},collectionEvents:{change:"change",sort:"sortChildren"},initialize:function(){this.wait();var e=this;this.model.distribution(function(o){e.model.values({limit:0},function(i){var n={};t.each(i.values,function(e){n[e.value]=e.label});var l=t.map(o.data,function(e){var t=e.values[0];return{count:e.count,value:t,label:n[t]}});e.collection.reset(l),e.ready()})})},calcTotal:function(){for(var e=0,t=this.collection.pluck("count"),o=0;o<t.length;o++)e+=t[o];return e},sortChildren:function(){var e=this;this.collection.each(function(t){var o=e.collection.findByModel(t);e.$el.append(o.el)})},getField:function(){return this.model.id},getOperator:function(){return this.collection.where({excluded:!0}).length>0?"-in":"in"},getValue:function(){return t.map(this.collection.where({selected:!0}),function(e){return e.get("value")})},setValue:function(e){e||(e=[]),this.collection.each(function(t){var o=t.get("value");t.set("selected",e.indexOf(o)>=0)})},setOperator:function(t){"-in"===t&&(this.collection.each(function(e){e.set("excluded",!0)}),e("input[name=exclude]").attr("checked",!0))}}),u=i.ItemView.extend({className:"navbar navbar-toolbar",template:"controls/infograph/toolbar",events:{"keyup [name=filter]":"filterBars","click [name=invert]":"invertSelection","click .sort-value-header, .sort-count-header":"sortBy","change [name=exclude]":"excludeCheckboxChanged"},ui:{toolbar:".btn-toolbar",filterInput:"[name=filter]",invertButton:"[name=invert]",sortValueHeader:".sort-value-header",sortCountHeader:".sort-count-header",excludeCheckbox:"[name=exclude]"},initialize:function(){this.sortDirection="-count"},sortBy:function(e){switch(this.sortDirection="sort-value-header"===e.currentTarget.className?"-value"===this.sortDirection?"value":"-value":"-count"===this.sortDirection?"count":"-count",this.sortDirection){case"-count":this.ui.sortValueHeader.html("Value <i class=icon-sort></i>"),this.ui.sortCountHeader.html("Count <i class=icon-sort-down></i>");break;case"count":this.ui.sortValueHeader.html("Value <i class=icon-sort></i>"),this.ui.sortCountHeader.html("Count <i class=icon-sort-up></i>");break;case"-value":this.ui.sortValueHeader.html("Value <i class=icon-sort-down></i>"),this.ui.sortCountHeader.html("Count <i class=icon-sort></i>");break;case"value":this.ui.sortValueHeader.html("Value <i class=icon-sort-up></i>"),this.ui.sortCountHeader.html("Count <i class=icon-sort></i>")}this.collection.sortModelsBy(this.sortDirection)},toggle:function(e){this.ui.filterInput.toggle(e),this.ui.invertButton.toggle(e),this.ui.sortValueHeader.toggle(e),this.ui.sortCountHeader.toggle(e)},filterBars:function(e){var o;t.isString(e)?o=e:(null!==e&&e.stopPropagation(),o=this.ui.filterInput.val());var i=new RegExp(o,"i");this.collection.each(function(e){e.set("visible",!o||i.test(e.get("value")))})},invertSelection:function(){this.collection.each(function(e){(e.get("visible")!==!1||e.get("selected"))&&e.set("selected",!e.get("selected"))}),this.collection.trigger("change")},excludeCheckboxChanged:function(){var e=this.ui.excludeCheckbox.prop("checked");this.collection.each(function(t){t.set("excluded",e,{silent:!0})}),this.collection.trigger("change:excluded")}}),h=n.ControlLayout.extend({template:"controls/infograph/layout",events:{change:"change"},options:{minValuesForToolbar:10},regions:{bars:".bars-region",toolbar:".toolbar-region"},ui:{loading:"[data-target=loading-indicator]"},collectionEvents:{reset:"toggleToolbar"},initialize:function(){t.bindAll(this,"toggleToolbar")},constructor:function(e){e.collection||(e.collection=new s),n.ControlLayout.prototype.constructor.apply(this,arguments),this.barsControl=new c({model:this.model,collection:this.collection});var o=this,i=["set","get","when","ready","wait"],l=function(e){return o[e]=function(){var t=o.barsControl;return t[e].apply(t,arguments)},o[e]};t.each(i,function(e){l(e)}),this.listenTo(this.barsControl,"all",function(){var e=arguments[0];("change"===e||"beforeready"===e||"ready"===e)&&this.trigger.apply(this,arguments),"ready"===e&&this.ui.loading.hide()})},toggleToolbar:function(){this.toolbar.currentView&&this.toolbar.currentView.toggle(this.collection.length>=this.options.minValuesForToolbar)},onRender:function(){this.bars.show(this.barsControl),this.toolbar.show(new u({collection:this.collection})),this.toggleToolbar()},validate:function(e){return t.isUndefined(e.value)||0===e.value.length?"Select at least one value":void 0}});return{InfographControl:h}});
//# sourceMappingURL=infograph.js.map