sap.ui.define([
    "./BaseController"
], function (BaseController) {
    "use strict";

    return BaseController.extend("codescale.radar.controller.VoiceAI", {
        onInit: function () {
            var oRouter = this.getRouter();
            oRouter.getRoute("voiceai").attachPatternMatched(this._onRouteMatched, this);
        },

        _onRouteMatched: function () {
            // Route matched handler
        }
    });
});
