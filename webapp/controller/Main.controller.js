sap.ui.define([
    "./BaseController",
    "sap/ui/model/json/JSONModel",
    "sap/m/MessageToast"
], function (BaseController, JSONModel, MessageToast) {
    "use strict";

    return BaseController.extend("codescale.radar.controller.Main", {
        onInit: function () {
            var oViewModel = new JSONModel({
                busy: false,
                signalCount: 0,
                noiseCount: 0,
                lastUpdated: "",
                selectedFocusArea: "all"
            });
            this.setModel(oViewModel, "view");

            var oRouter = this.getRouter();
            oRouter.getRoute("main").attachPatternMatched(this._onRouteMatched, this);
        },

        _onRouteMatched: function () {
            this._updateCounts();
        },

        _updateCounts: function () {
            var oViewModel = this.getModel("view");
            var oRadarModel = this.getModel("radar");

            if (oRadarModel) {
                var aItems = oRadarModel.getProperty("/items") || [];
                var nSignalCount = aItems.filter(function (item) {
                    return item.classification === "signal";
                }).length;
                var nNoiseCount = aItems.filter(function (item) {
                    return item.classification === "noise";
                }).length;

                oViewModel.setProperty("/signalCount", nSignalCount);
                oViewModel.setProperty("/noiseCount", nNoiseCount);
                oViewModel.setProperty("/lastUpdated", new Date().toLocaleString());
            }
        },

        onFocusAreaSelect: function (oEvent) {
            var sKey = oEvent.getParameter("key");
            var oViewModel = this.getModel("view");
            oViewModel.setProperty("/selectedFocusArea", sKey);
        },

        onFilterPress: function () {
            var oBundle = this.getResourceBundle();
            MessageToast.show(oBundle.getText("filterNotImplemented"));
        }
    });
});
