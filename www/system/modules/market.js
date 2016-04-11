chimera.system.market = angular.module("market", ["ngResource", "ngSanitize"]);

chimera.system.market.controller("CartController", ["$scope", "cartService",
    function ($scope, cartService) {
        // Информация по корзине.
        $scope.cart = {};
        if ($scope.user.auth) {
            cartService.get({}, function(response) {
                $scope.cart = response;
            });
        }
    }
]);

chimera.system.market.controller("OrderController", ["$scope", "$state", "cartService",
    function ($scope, $state, cartService) {
        // Информация по корзине.
        $scope.cart = {};
        cartService.get({}, function(response) {
            $scope.cart = response;
        });

        // Добавит 1 единицу товара.
        $scope.plusProductButton = function(productId) {
            cartService.save({product: productId, change: 1}, function(response) {
                $scope.cart = response;
            });
        }
        // Уберет 1 единицу товара.
        $scope.minusProductButton = function(productId) {
            cartService.save({product: productId, change: -1}, function(response) {
                $scope.cart = response;
            });
        }
        // Уберет товар из заказа.
        $scope.deleteProductButton = function(productId, change) {
            cartService.save({product: productId, change: -change}, function(response) {
                $scope.cart = response;
            });
        };
        // Подтверждение заказа.
        $scope.confirmOrderButton = function() {
            cartService.confirm({}, function(response) {
                $state.go("main.profile");
            });
        }
    }
]);

chimera.system.market.controller("CatalogItemController", ["$scope", "$state", "catalogItemService", "cartService",
    function ($scope, $state, catalogItemService, cartService) {
        var page = $state.params.page;
        $scope.catalog = {
            title: "Общий каталог",
            alias: "some"
        };
        $scope.cart = {};

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

        // Информация по корзине.
        if ($scope.user.auth) {
            cartService.get({}, function(response) {
                $scope.cart = response;
                $scope.$apply();
            });
        }

        // Добавить товар в корзину.
        $scope.addToCart = function(productId) {
            if ($scope.user.auth) {
                cartService.save({product: productId}, function(response) {
                    $scope.cart = response;
                    $scope.$apply();
                });
            } else {
                $.notify("Вам необходимо войти в систему под зарегистрированной учетной записью");
            }
        }
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

chimera.system.market.factory("cartService", ["$resource",
    function ($resource) {
        return $resource("/cart", null, {
            "confirm": {method:"PUT"}
        });
    }
]);