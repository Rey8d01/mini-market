/**
 * Модуль магазина.
 * Работа с корзиной, поиск и оформление заказа.
 */
chimera.system.market = angular.module("market", ["ngResource", "ngSanitize"]);

// Информация по корзине.
chimera.system.market.controller("CartInfoController", ["$scope", "cartService",
    function ($scope, cartService) {
        $scope.cart = {};
        if ($scope.user.auth) {
            cartService.get({}, function(response) {
                $scope.cart = response;
            });
        }
    }
]);

// Оформление заказа.
chimera.system.market.controller("CartController", ["$scope", "$state", "cartService",
    function ($scope, $state, cartService) {
        var calculateAmount = function(products) {
            amount = 0;
            for (i in products) {
                product = products[i];
                amount += product.count_product * product.amount;
            }
            console.log(amount);
            return amount;
        };
        // Информация по корзине.
        $scope.cart = {};
        $scope.calculateAmount = 10;
        cartService.get({}, function(response) {
            $scope.cart = response;
            $scope.calculateAmount = calculateAmount(response.products);
        });

        // Добавит 1 единицу товара.
        $scope.plusProductButton = function(productId) {
            cartService.save({product: productId, change: 1}, function(response) {
                $scope.cart = response;
                $scope.calculateAmount = calculateAmount(response.products);
            });
        }
        // Уберет 1 единицу товара.
        $scope.minusProductButton = function(productId) {
            cartService.save({product: productId, change: -1}, function(response) {
                $scope.cart = response;
                $scope.calculateAmount = calculateAmount(response.products);
            });
        }
        // Уберет товар из заказа.
        $scope.deleteProductButton = function(productId, change) {
            cartService.save({product: productId, change: -change}, function(response) {
                $scope.cart = response;
                $scope.calculateAmount = calculateAmount(response.products);
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
            });
        }

        // Добавить товар в корзину.
        $scope.addToCart = function(productId) {
            if ($scope.user.auth) {
                cartService.save({product: productId}, function(response) {
                    $scope.cart = response;
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
        return $resource("/catalog-products/:catalogAlias", {catalogAlias: "some", page: "1"});
    }
]);

chimera.system.market.factory("catalogListService", ["$resource",
    function ($resource) {
        return $resource("/catalog-list");
    }
]);

// Сервис по оформлению нового заказа.
chimera.system.market.factory("cartService", ["$resource",
    function ($resource) {
        return $resource("/cart", null, {
            "confirm": {method:"PUT"}
        });
    }
]);

// Сервис по работе с существующими заказами.
chimera.system.market.factory("orderService", ["$resource",
    function ($resource) {
        return $resource("/order/:orderId", {orderId: null});
    }
]);