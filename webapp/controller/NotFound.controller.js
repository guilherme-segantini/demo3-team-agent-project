sap.ui.define([
    "./BaseController"
], function (BaseController) {
    "use strict";

    return BaseController.extend("codescale.radar.controller.NotFound", {
        onInit: function () {
            // Not Found controller
        },

        onNavHome: function () {
            this.getRouter().navTo("main");
        }
    });
});
