chimera.system.main.directive('listProducts', function () {
    return {
        restrict: 'EA',
        scope: {
            products: '=',
            paginationData: '=',
            addToCart: '=',
            state: '@',
            catalogAlias: '='
        },
        templateUrl: "/system/templates/listProducts.html"
    };
});