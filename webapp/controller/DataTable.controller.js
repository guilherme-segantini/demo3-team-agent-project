sap.ui.define([
    "./BaseController",
    "sap/ui/model/json/JSONModel",
    "sap/ui/model/Filter",
    "sap/ui/model/FilterOperator",
    "sap/ui/model/Sorter",
    "../model/formatter"
], function (BaseController, JSONModel, Filter, FilterOperator, Sorter, formatter) {
    "use strict";

    return BaseController.extend("codescale.radar.controller.DataTable", {
        formatter: formatter,

        onInit: function () {
            var oViewModel = new JSONModel({
                itemCount: 0,
                sortDescending: true,
                currentSortField: "confidence_score"
            });
            this.setModel(oViewModel, "view");

            this.getRouter().getRoute("dataTable").attachPatternMatched(this._onRouteMatched, this);
        },

        _onRouteMatched: function () {
            this._updateItemCount();
        },

        _updateItemCount: function () {
            var oTable = this.byId("trendTable");
            if (oTable) {
                var oBinding = oTable.getBinding("items");
                if (oBinding) {
                    var iCount = oBinding.getLength();
                    this.getModel("view").setProperty("/itemCount", iCount);
                }
            }
        },

        onRefreshTable: function () {
            var oRadarModel = this.getModel("radar");
            if (oRadarModel) {
                oRadarModel.refresh(true);
                this._updateItemCount();
            }
        },

        onSearch: function (oEvent) {
            var sQuery = oEvent.getParameter("query") || oEvent.getParameter("newValue") || "";
            this._applyFilters(sQuery);
        },

        onFilterChange: function () {
            var sSearchValue = this.byId("searchField").getValue();
            this._applyFilters(sSearchValue);
        },

        _applyFilters: function (sSearchValue) {
            var aFilters = [];
            var oTable = this.byId("trendTable");
            var oBinding = oTable.getBinding("items");

            // Search filter
            if (sSearchValue) {
                var oSearchFilter = new Filter({
                    filters: [
                        new Filter("tool_name", FilterOperator.Contains, sSearchValue),
                        new Filter("technical_insight", FilterOperator.Contains, sSearchValue)
                    ],
                    and: false
                });
                aFilters.push(oSearchFilter);
            }

            // Focus area filter
            var sFocusArea = this.byId("focusAreaFilter").getSelectedKey();
            if (sFocusArea && sFocusArea !== "all") {
                aFilters.push(new Filter("focus_area", FilterOperator.EQ, sFocusArea));
            }

            // Classification filter
            var sClassification = this.byId("classificationFilter").getSelectedKey();
            if (sClassification && sClassification !== "all") {
                aFilters.push(new Filter("classification", FilterOperator.EQ, sClassification));
            }

            // Apply combined filters
            var oCombinedFilter = aFilters.length > 0 ? new Filter({ filters: aFilters, and: true }) : [];
            oBinding.filter(oCombinedFilter);

            this._updateItemCount();
        },

        onSortByConfidence: function () {
            this._sortTable("confidence_score");
        },

        onSortByName: function () {
            this._sortTable("tool_name");
        },

        _sortTable: function (sField) {
            var oTable = this.byId("trendTable");
            var oBinding = oTable.getBinding("items");
            var oViewModel = this.getModel("view");

            var sCurrentField = oViewModel.getProperty("/currentSortField");
            var bDescending = oViewModel.getProperty("/sortDescending");

            // Toggle direction if same field, otherwise default to descending for confidence, ascending for name
            if (sCurrentField === sField) {
                bDescending = !bDescending;
            } else {
                bDescending = sField === "confidence_score";
            }

            oViewModel.setProperty("/sortDescending", bDescending);
            oViewModel.setProperty("/currentSortField", sField);

            var oSorter = new Sorter(sField, bDescending);
            oBinding.sort(oSorter);
        },

        onItemSelect: function (oEvent) {
            var oItem = oEvent.getParameter("listItem");
            if (oItem) {
                var oContext = oItem.getBindingContext("radar");
                if (oContext) {
                    var oData = oContext.getObject();
                    this._showItemDetails(oData);
                }
            }
        },

        onItemPress: function (oEvent) {
            var oItem = oEvent.getSource();
            var oContext = oItem.getBindingContext("radar");
            if (oContext) {
                var oData = oContext.getObject();
                this._showItemDetails(oData);
            }
        },

        _showItemDetails: function (oData) {
            // Navigate to detail view or show dialog
            // For now, we just log the selection - can be extended to navigate to detail page
            var sToolName = oData.tool_name;
            var iIndex = this._findTrendIndex(sToolName);
            if (iIndex !== -1) {
                this.navTo("trendDetail", { index: iIndex });
            }
        },

        _findTrendIndex: function (sToolName) {
            var oRadarModel = this.getModel("radar");
            var aTrends = oRadarModel.getProperty("/trends") || [];
            for (var i = 0; i < aTrends.length; i++) {
                if (aTrends[i].tool_name === sToolName) {
                    return i;
                }
            }
            return -1;
        }
    });
});
