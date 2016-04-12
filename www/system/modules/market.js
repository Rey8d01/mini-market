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

// Просмотр отдельного каталога, фильтрация по тегам и выбор товаров в корзину
chimera.system.market.controller("CatalogItemController", ["$scope", "$state", "catalogItemService", "cartService", "productsService", "tagsService",
    function ($scope, $state, catalogItemService, cartService, productsService, tagsService) {
        $scope.catalog = {};
        $scope.products = {};
        $scope.pageData = {};
        $scope.cart = {};
        $scope.tags = {};
        $scope.filtersCheckbox = {};

        var page = $state.params.page,
            // Запрос на информацию по товарам - отдельная функция для реагирования на изменения в фильтрах.
            getProducts = function() {
                var tags = _.reduce($scope.filtersCheckbox, function(memo, value, key) { if (value) { memo.push(key); } return memo; }, []);
                $scope.main.blogContentLoad = true;
                productsService.get({aliasCatalog: $state.params.aliasCatalog, page: $state.params.page, tags: tags}, function (response) {
                    $scope.pageData = {
                        pageSize: 5,
                        total: response.count,
                        currentPage: page
                    };
                    $scope.products = response.results;
                    $scope.main.blogContentLoad = false;
                });
            }

        // Информация по текущему каталогу.
        catalogItemService.get({aliasCatalog: $state.params.aliasCatalog}, function (response) {
            $scope.catalog = response;
        });
        // Информация по всем тегам.
        tagsService.get({}, function (response) {
            for (item in response.results) {
                tag = response.results[item];
                $scope.tags[tag.title] = tag.alias;
                $scope.filtersCheckbox[tag.alias] = false;
            }
//            $scope.tags = response.results;
        });
        // Информация по списку товаров.
        getProducts();
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
        // Изменение фильтров - запрос на новый поиск.
        $scope.changeFilter = function() {
            getProducts();
        }
    }
]);

chimera.system.market.controller("CatalogListController", ["$scope", "$state", "catalogListService", "cartService",
    function ($scope, $state, catalogListService, cartService) {
//        var page = $state.params.page;
        $scope.catalogs = [];
        $scope.cart = {};

        $scope.main.blogContentLoad = true;
        catalogListService.get({}, function (response) {
            $scope.catalogs = response.results;
            $scope.main.blogContentLoad = false;
        });

        // Информация по корзине.
        if ($scope.user.auth) {
            cartService.get({}, function(response) {
                $scope.cart = response;
            });
        }
    }
]);

// Справочные сервисы по каталогам, тегам и товарам.
chimera.system.market.factory("productsService", ["$resource",
    function ($resource) {
        return $resource("/products/:aliasCatalog", {aliasCatalog: null, page: "1"});
    }
]);

chimera.system.market.factory("catalogItemService", ["$resource",
    function ($resource) {
        return $resource("/catalog-item/:aliasCatalog");
    }
]);

chimera.system.market.factory("catalogListService", ["$resource",
    function ($resource) {
        return $resource("/catalog-list");
    }
]);

chimera.system.market.factory("tagsService", ["$resource",
    function ($resource) {
        return $resource("/tags");
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