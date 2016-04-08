(function(){

  angular.module('stockWatch.controllers')
    .controller('companyDetailsController', companyDetailsController);

  companyDetailsController.$inject = ['$scope','Layout','$interval','$window','$timeout','$stateParams'];

  function companyDetailsController($scope,Layout, $interval,$window,$timeout,$stateParams){

    var vm = this;
    
    console.log("I am called...",$stateParams);
  };
})();