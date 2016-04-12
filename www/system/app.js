/**
 *  App Module
 *
 *  Основной модуль - с конфигурациями и настройками.
 */

/**
 * Общий объект системы
 */
var chimera = {
    config: {
        baseUrl: "http://www.mini-market.local/_",
        baseWWWUrl: "http://www.mini-market.local"
    },
    system: {}
};


chimera.system.main = angular.module("main", [
    "ui.router",
    "market",
    "user",
]);

/**
 * Перехват входящих/исходящих запросов.
 */
chimera.system.main.factory("sessionRecover", ["$q", "$location", function ($q, $location) {
    // Общая обработка ошибок.
    var parseError = function (error) {
        switch (error.code) {
            case 11:
                $.notify(error.message, "error");
                $location.path("/signin").replace();
                break;
            default:
                $.notify(error.message, "error");
                break;
        }
    };

    return {
        /**
         * Роутинг запросов по статике и к системе.
         *
         * @param config
         * @returns {*}
         */
        request: function (config) {
            if (!s.startsWith(config.url, "//")) {
                // Внешние запросы остаются без модификаций.
                if (/.*\.(js|css|ico|htm|html|json)/.test(config.url)) {
                    // Запросы по статик файлам переадресуются на основной домен.
                    config.url = chimera.config.baseWWWUrl + config.url;
                } else {
                    // Запросы не относящиея к статик файлам идут к основной системе.
                    config.url = chimera.config.baseUrl + config.url;
                }
            }

            return config;
        },
        /**
         * Разбор ответов для определения соответствующей реакции на случай возникновения ошибок.
         *
         * @param response
         * @returns {*}
         */
        response: function (response) {
            return response;
        },
        responseError: function (rejection) {
            var data = rejection.data;

            if (data && data.detail) {
                $.notify(data.detail, "error");
            } else {
                $.notify("Что то пошло не так", "error");
            }

            return $q.reject(rejection);
        }
    };
}]);

chimera.system.main.config(["$stateProvider", "$urlRouterProvider", "$locationProvider", "$httpProvider",
    function ($stateProvider, $urlRouterProvider, $locationProvider, $httpProvider) {
        // Перехват всех http запросов для определения ошибок и реакции на них.
        $httpProvider.interceptors.push("sessionRecover");

        // https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        // html5Mode - без # в урле
        $locationProvider.html5Mode({
            enabled: true,
            requireBase: false
        });

        // Любые неопределенные url перенаправлять на страницу авторизации (при успешной авторизации произойдет редирект).
        $urlRouterProvider.otherwise("/home");


        // Определение состояний для всего приложения.
        $stateProvider
        /**
         * Форма входа.
         */
            .state("signin", {
                url: "/signin",
                views: {
                    "": {
                        templateUrl: "/system/templates/signin.html",
                        controller: "AuthController"
                    }
                }
            })
            .state("signup", {
                url: "/signup",
                views: {
                    "": {
                        templateUrl: "/system/templates/signup.html",
                        controller: "AuthController"
                    }
                }
            })
        /**
         * Главное абстрактное состояние для системы. Включает в себя компоненты авторизованного пользователя
         * и основную контентную область.
         */
            .state("main", {
                abstract: true,
                url: "",
                views: {
                    "": {
                        templateUrl: "/system/templates/main.html",
                        controller: "ChimeraController"
                    }
                }
            })
            .state("main.home", {
                url: "/home",
                views: {
                    "content": {
                        templateUrl: "/system/templates/catalogList.html",
                        controller: "CatalogListController"
                    }
                }
            })
            .state("main.catalog", {
                url: "/catalog/:aliasCatalog/:page",
                params: {
                    "page": "1"
                },
                views: {
                    "content": {
                        templateUrl: "/system/templates/catalogItem.html",
                        controller: "CatalogItemController"
                    },
                }
            })
            .state("main.profile", {
                url: "/profile",
                views: {
                    "content": {
                        templateUrl: "/system/templates/profile.html",
                        controller: "UserController"
                    },
                }
            })
            .state("main.order", {
                url: "/order",
                views: {
                    "content": {
                        templateUrl: "/system/templates/order.html",
                        controller: "CartController"
                    },
                }
            })
        ;

    }
]);

/**
 * Базовый контроллер.
 */
chimera.system.main.controller("ChimeraController", ["$scope", "$state", "authService", "cartService",
    function ($scope, $state, authService, cartService) {
        $scope.main = {
            "title": "Mini-market",
            "contentLoad": false,
            "foo": "BAAAAAR"
        };

        // Пользовательская информация.
        $scope.user = {
            auth: false,
            data: {}
        };

        authService.status().then(function (response) {
            $scope.user = {
                auth: true,
                data: response.auth
            };

            // После авторизации получение дополнительной информации - по корзине
            cartService.get({}, function(response) {
                $scope.cart = response;
            });
        }, function (response) {
            $scope.user = {
                auth: false,
                data: {}
            };
        });

        $scope.signoutButton = function () {
            authService.signout();
            $state.go("signin");
            $scope.user = {
                auth: false,
                data: {}
            };
        };
    }
]);
