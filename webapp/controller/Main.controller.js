sap.ui.define([
    "./BaseController",
    "sap/ui/model/json/JSONModel"
], function (BaseController, JSONModel) {
    "use strict";

    return BaseController.extend("codescale.radar.controller.Main", {
        onInit: function () {
            var oViewModel = new JSONModel({
                busy: false,
                radarDate: ""
            });
            this.setModel(oViewModel, "view");
        },

        onRefresh: function () {
            var oRadarModel = this.getModel("radar");
            if (oRadarModel) {
                oRadarModel.refresh(true);
            }
        }
    });
});
