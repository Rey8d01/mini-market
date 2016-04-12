/**
 * Пользовательский модуль.
 * Включает в себя работу с авторизацией, регистрацией и работу профилем пользователя.
 */
chimera.system.user = angular.module("user", ["ngResource", "ngSanitize"]);

// Заполнение профильной информации авторизованного пользователя.
chimera.system.user.controller("UserController", ["$scope", "$state", "userService", "orderService",
    function ($scope, $state, userService, orderService) {
        $scope.orders = {};
        orderService.get({}, function(response) {
            $scope.orders = response.results;
        });

        // Сохранение пользовательской информации.
        $scope.saveUserInfoButton = function () {
            userService.update($scope.user.data, function (response) {
                $.notify("Информация сохранена", "success");
            });
        }

        // Отмена заказа.
        $scope.cancelOrderButton = function(orderId) {
            orderService.delete({orderId: orderId}, function(response) {
                $state.go("main.profile");
            });
        }
    }
]);

// Контроллер для авторизации и регистрации.
chimera.system.user.controller("AuthController", ["$scope", "$state", "authService",
    function ($scope, $state, authService) {
        $scope.email = "";
        $scope.password = "";
        $scope.passwordConfirm = "";

        $scope.signupButton = function () {
            if ($scope.password == $scope.passwordConfirm) {
                authService.signup($scope.email, $scope.password, $scope.passwordConfirm).then(function (response) {
                    $state.go("main.home");
                });
            } else {
                $.notify("Поля подтверждение и пароль не совпдают", "error");
            }
        };

        $scope.signinButton = function () {
            authService.signin($scope.email, $scope.password).then(function (response) {
                $state.go("main.home");
            });
        };
    }
]);

// Сервис для сохранения информации по профилю пользователя.
chimera.system.user.factory("userService", ["$resource",
    function ($resource) {
        return $resource("/profile", null, {
            "update": {method:"PUT"}
        });
    }
]);

// Сервис авторизации/регистрации.
chimera.system.user.factory("authService", ["$q", "$http",
    function ($q, $http) {
        // Общая функция успешной обработки для всех запросов авторизации.
        var fnSuccess = function(deferred) {
            return function (data, status, headers, config) {
                if (data && data.auth) {
                    deferred.resolve(data);
                } else {
                    deferred.reject(data);
                }
            };
        };

        return {
            // Авторизация.
            signin: function (email, password) {
                var deferred = $q.defer();
                $http.post("/auth", {email: email, password: password}).success(fnSuccess(deferred));
                return deferred.promise;
            },
            // Регистрация.
            signup: function (email, password, passwordConfirm) {
                var deferred = $q.defer();
                $http.put("/auth", {email: email, password: password, passwordConfirm: passwordConfirm}).success(fnSuccess(deferred));
                return deferred.promise;
            },
            // Выход.
            signout: function () {
                $http.delete("/auth");
            },
            // Проверка статуса авторизации.
            status: function() {
                var deferred = $q.defer();
                $http.get("/auth").success(fnSuccess(deferred));
                return deferred.promise;
            }
        };
    }
]);
