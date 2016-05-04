(function(){

  angular.module('stockWatch.controllers')
    .controller('headController', headController);

  headController.$inject = ['$scope','$rootScope'];

  function headController($scope,$rootScope){

    var vm = this;
    vm.pagetitle = "Portfolio"; 
    $scope.pagetitle = "Portfolio";
    $rootScope.portfolio_change = "";
    
    $scope.$watch(function(){ return $rootScope.portfolio_change}, function(){
      $scope.pagetitle = "Portfolio " + $rootScope.portfolio_change;
    });
  };
})();