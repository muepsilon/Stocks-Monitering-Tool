(function(){

  angular.module('stockWatch.controllers')
    .controller('headController', headController);

  headController.$inject = ['$scope','$rootScope'];

  function headController($scope,$rootScope){

    var vm = this;
    vm.dailyChangeLastVal = 0;
    vm.portfolioChange = [];
    vm.pagetitle = "Portfolio";
    $scope.pagetitle = "Portfolio";
    $rootScope.portfolio_change = "";
    
    $scope.$watch(function(){ return $rootScope.portfolio_change}, function(){
      $scope.pagetitle = "Portfolio " + $rootScope.portfolio_change;
      // Notification system
      vm.portfolioChange = $rootScope.portfolio_change.split("/").map(Number); 
      vm.baseChange = Math.abs(vm.portfolioChange[1]) > 1000 ? vm.portfolioChange[1] : 1000;

      if (Math.abs((vm.portfolioChange[0]-vm.dailyChangeLastVal)/vm.baseChange)*100 > 10) {
        console.log(vm.portfolioChange[0],vm.dailyChangeLastVal, vm.baseChange);
        
        if (Notification.permission == "granted") {
          if (vm.portfolioChange[0] > 0) {
            var notification = new Notification('Profit', {
              icon: 'https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/shopping-circle-green-128.png',
              body: $scope.pagetitle,
            });
          } else {
            var notification = new Notification('Loss', {
              icon: 'http://www.iconsdb.com/icons/preview/soylent-red/sell-2-xxl.png',
              body: $scope.pagetitle,
            });
          }
        }

        vm.dailyChangeLastVal = vm.portfolioChange[0];
      };
    });
  };
})();