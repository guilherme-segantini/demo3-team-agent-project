sap.ui.define([
    "./BaseController"
], function (BaseController) {
    "use strict";

    return BaseController.extend("codescale.radar.controller.AgentOrch", {
        onInit: function () {
            var oRouter = this.getRouter();
            oRouter.getRoute("agentorch").attachPatternMatched(this._onRouteMatched, this);
        },

        _onRouteMatched: function () {
            // Route matched handler
        }
    });
});
