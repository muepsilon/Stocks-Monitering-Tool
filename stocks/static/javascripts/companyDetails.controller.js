(function(){

  angular.module('stockWatch.controllers')
    .controller('companyDetailsController', companyDetailsController);

  companyDetailsController.$inject = ['$scope','Layout','$interval','$window','$timeout','$stateParams','$state'];

  function companyDetailsController($scope,Layout, $interval,$window,$timeout,$stateParams, $state){

    var vm = this;
    var companyName = $stateParams['name'].replace(/[-]/g,' ');
    
    vm.showPage = false;
    vm.isValidCompany = null;
    vm.companyData = null;
    vm.companySymbol = null; 

    Layout.validate_company_name(companyName)
    .then(function successCallback(response){
      
      if (response.data.length == 0) {
        vm.showPage = true;
        vm.isValidCompany = false;
        setTimeout(function(){$state.go('home')},3000);
      
      } else {
        
        vm.isValidCompany = true;
        vm.companySymbol = response.data[0].symbol;

        Layout.get_company_data(vm.companySymbol)
        .then(function successCallback(response){
          vm.showPage = true;
          vm.companyData = response.data;
            
        },function failureCallback(response){
          
        });

      }
    },function failureCallback(response){
      vm.showPage = true;
      vm.isValidCompany = false;
      setTimeout(function(){$state.go('home')},3000);
    });

  };
})();