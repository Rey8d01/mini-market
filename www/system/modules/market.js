chimera.system.market = angular.module("market", ["ngResource", "ngSanitize"]);

chimera.system.market.controller("CatalogItemController", ["$scope", "$state", "catalogItemService",
    function ($scope, $state, catalogItemService) {
        $scope.catalog = {
            title: "Общий каталог",
            alias: "some"
        };
        var page = $state.params.page;

        $scope.main.blogContentLoad = true;
//        catalogItemService.get({catalogAlias: $state.params.catalogAlias, page: $state.params.page}, function (response) {
        catalogItemService.get({page: page}, function (response) {
            $scope.catalog.pageData = {
                pageSize: 2,
                total: response.count,
                currentPage: page
            };
            $scope.catalog.products = response.results;
            $scope.main.blogContentLoad = false;
        });
    }
]);

chimera.system.market.controller("CatalogListController", ["$scope", "$state", "catalogListService",
    function ($scope, $state, catalogListService) {

    }
]);

chimera.system.market.factory("catalogItemService", ["$resource",
    function ($resource) {
        return $resource("/catalog-item/:catalogAlias", {catalogAlias: "some", page: "1"});
    }
]);

chimera.system.market.factory("catalogListService", ["$resource",
    function ($resource) {
        return $resource("/catalog-list");
    }
]);