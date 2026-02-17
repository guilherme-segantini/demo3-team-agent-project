sap.ui.define([
    "./BaseController",
    "sap/ui/model/json/JSONModel"
], function (BaseController, JSONModel) {
    "use strict";

    return BaseController.extend("codescale.radar.controller.App", {
        onInit: function () {
            var oViewModel = new JSONModel({
                sideExpanded: true
            });
            this.setModel(oViewModel, "appView");
        },

        onSideNavToggle: function () {
            var oToolPage = this.byId("toolPage");
            var bExpanded = oToolPage.getSideExpanded();
            oToolPage.setSideExpanded(!bExpanded);
        },

        onNavigationSelect: function (oEvent) {
            var sKey = oEvent.getParameter("item").getKey();
            var oRouter = this.getRouter();

            switch (sKey) {
                case "radar":
                    oRouter.navTo("main");
                    break;
                case "voiceai":
                    oRouter.navTo("voiceai");
                    break;
                case "agentorch":
                    oRouter.navTo("agentorch");
                    break;
                case "durableruntime":
                    oRouter.navTo("durableruntime");
                    break;
                case "settings":
                    oRouter.navTo("settings");
                    break;
                default:
                    oRouter.navTo("main");
            }
        },

        onRefresh: function () {
            var oRadarModel = this.getModel("radar");
            if (oRadarModel) {
                oRadarModel.refresh(true);
            }
        }
    });
});
