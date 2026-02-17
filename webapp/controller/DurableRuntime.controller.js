sap.ui.define([
    "./BaseController"
], function (BaseController) {
    "use strict";

    return BaseController.extend("codescale.radar.controller.DurableRuntime", {
        onInit: function () {
            var oRouter = this.getRouter();
            oRouter.getRoute("durableruntime").attachPatternMatched(this._onRouteMatched, this);
        },

        _onRouteMatched: function () {
            // Route matched handler
        }
    });
});
