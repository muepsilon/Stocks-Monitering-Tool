// Companies controllers

(function(){

  angular.module('stockWatch.controllers')
    .controller('companiesController', companiesController);

  companiesController.$inject = ['$scope','Layout','$state'];

  function companiesController($scope,Layout,$state){

    var vm = this;
    vm.showPage = true;
    vm.stocks = [];
    vm.getStocks = getStocks;
    vm.clearFilters = clearFilters;
    $scope.items_per_page = 10;
    $scope.maxSize = 5;
    $scope.bigTotalItems = 1;
    $scope.bigCurrentPage = 1;
    vm.companyquery = null;
    vm.filters = {
      'price_by_book' : "Price/Book", 
      // 'eps' : "Earning/Share", 
      'p_by_e': "Price/Earning",
      'market_cap': "Market Capital",
      'div_perc' : "Dividend Percentage",
      'put_by_call' : "Put By Call Ratio",
      'p_by_e_relative': "P/E Relative"
    }
    
    vm.fields = {
      'company': "Company",
      'market_cap': "Market Capital(Cr)",
      "book_value": "Book Value",
      'price_by_book' : "Price/Book", 
      'eps' : "Earning/Share", 
      'p_by_e': "Price/Earning",
      'industry_p_by_e': 'Industry P/E',
      'div_perc' : "Dividend(%)",
      'put_by_call' : "Put/Call"
    }
    // Processed variables
    vm.filter_values = {};
    for (var key in vm.filters ) {
      vm.filter_values[key] = [null,null]
    }
    // Function Blocks
    function clearFilters(){
      // Reset all fitler values
      for (var key in vm.filters ) {
      vm.filter_values[key] = [null,null]
    }
    }
    function getStocks(){
      Layout.search_companies(vm.filter_values, vm.companyquery)
      .then(function successCallback (response) {
        vm.stocks = response.data;
        for (var i = vm.stocks.length - 1; i >= 0; i--) {
          vm.stocks[i]['company'] = vm.stocks[i]['company']['name'];
        };
        $scope.bigTotalItems = vm.stocks.length;
      }, function failureCallback (response) {
        // body...
      })
    }
     
  };
})();