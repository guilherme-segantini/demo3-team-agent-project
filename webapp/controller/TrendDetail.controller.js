sap.ui.define([
    "./BaseController",
    "sap/ui/model/json/JSONModel",
    "../model/formatter"
], function (BaseController, JSONModel, formatter) {
    "use strict";

    return BaseController.extend("codescale.radar.controller.TrendDetail", {
        formatter: formatter,

        onInit: function () {
            var oViewModel = new JSONModel({
                toolName: "",
                focusArea: "",
                classification: "",
                confidenceScore: 0,
                technicalInsight: "",
                signalEvidence: [],
                noiseIndicators: []
            });
            this.setModel(oViewModel, "view");

            this.getRouter().getRoute("trendDetail").attachPatternMatched(this._onRouteMatched, this);
        },

        _onRouteMatched: function (oEvent) {
            var sIndex = oEvent.getParameter("arguments").index;
            var iIndex = parseInt(sIndex, 10);

            var oRadarModel = this.getModel("radar");
            var aTrends = oRadarModel.getProperty("/trends") || [];

            if (iIndex >= 0 && iIndex < aTrends.length) {
                var oTrend = aTrends[iIndex];
                this._bindTrendData(oTrend);
            } else {
                this.navTo("dataTable");
            }
        },

        _bindTrendData: function (oTrend) {
            var oViewModel = this.getModel("view");
            oViewModel.setProperty("/toolName", oTrend.tool_name || "");
            oViewModel.setProperty("/focusArea", this.formatter.formatFocusArea(oTrend.focus_area));
            oViewModel.setProperty("/classification", oTrend.classification || "");
            oViewModel.setProperty("/confidenceScore", oTrend.confidence_score || 0);
            oViewModel.setProperty("/technicalInsight", oTrend.technical_insight || "");
            oViewModel.setProperty("/signalEvidence", oTrend.signal_evidence || []);
            oViewModel.setProperty("/noiseIndicators", oTrend.noise_indicators || []);
        }
    });
});
