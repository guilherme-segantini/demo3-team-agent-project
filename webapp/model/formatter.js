sap.ui.define([], function () {
    "use strict";

    return {
        classificationState: function (sClassification) {
            if (sClassification === "signal") {
                return "Success";
            } else if (sClassification === "noise") {
                return "None";
            }
            return "None";
        },

        classificationIcon: function (sClassification) {
            if (sClassification === "signal") {
                return "sap-icon://accept";
            } else if (sClassification === "noise") {
                return "sap-icon://decline";
            }
            return "sap-icon://question-mark";
        },

        confidenceText: function (iScore) {
            if (iScore >= 90) {
                return "High";
            } else if (iScore >= 70) {
                return "Medium";
            }
            return "Low";
        },

        focusAreaText: function (sFocusArea) {
            var oMap = {
                "voice_ai_ux": "Voice AI UX",
                "agent_orchestration": "Agent Orchestration",
                "durable_runtime": "Durable Runtime"
            };
            return oMap[sFocusArea] || sFocusArea;
        }
    };
});
