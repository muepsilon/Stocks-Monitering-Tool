// Index controllers

(function(){

  angular.module('stockWatch.controllers')
    .controller('indexController', indexController);

  indexController.$inject = ['$scope','Layout','$interval','$window','$timeout','$http','$rootScope'];

  function indexController($scope,Layout, $interval,$window,$timeout,$http,$rootScope){

    var vm = this;
    vm.showpage = false;
    vm.get_stocks = get_stocks;
    vm.get_watchlist = get_watchlist;
    vm.addOption = "new";
    vm.refresh = refresh;
    vm.refreshOption = [30,60,60*2,60*5,60*10,60*15,60*30];
    vm.refreshOptionList = [];
    vm.createRefreshOptionList = createRefreshOptionList;
    vm.alert = {"success": false, "failure": false, "message": ""};
    vm.show_alert = alert;
    vm.notification_text_high = "";
    vm.notification_text_low = "";
    vm.process = {"updating": false};
    vm.clearSelected = clearSelected;
    vm.delete_stock = delete_stock;
    vm.delete_stock_watch_list = delete_stock_watch_list;
    vm.addToExisting = addToExisting;
    vm.addStock =  add_stock;
    vm.addWatchStock = add_watch_stock;
    vm.editStock = editStock;
    vm.sellStock = sellStock;
    vm.editStockWatchList = editStockWatchList;
    vm.stock_operation = "";
    vm.stock_id = 0;
    vm.date = new Date();
    vm.formdata = {};
    vm.formdata.symbol = "";
    vm.formdata.company_name = "";
    vm.portfolio = {};
    vm.portfolio.invested_amount = 0;
    vm.portfolio.daily_change = 0;
    vm.portfolio.daily_change_percent = 0;
    vm.portfolio.change = 0;
    vm.portfolio.percent_change = 0;
    vm.portfolio.latestValue = 0;
    vm.selected_stock = "";
    vm.get_stocks();
    vm.get_watchlist();
    $scope.dropdown = {"search": true };
    vm.companySuggestion = [];
    vm.selectCompany = selectCompany;
    vm.showSearchSuggetsion = showSearchSuggetsion;
    vm.createRefreshOptionList();
    vm.duringExhangeOpen = duringExhangeOpen;
    vm.searchSuggestion = searchSuggestion;
    vm.setInterval = vm.refreshOptionList[2];
    $interval(vm.duringExhangeOpen, 1000*vm.refreshOption[vm.setInterval.id]);

    // Function blocks
    function searchSuggestion(){
      if (vm.formdata.company_name != undefined && vm.formdata.company_name.length > 0) {
        Layout.validate_company_name(vm.formdata.company_name)
        .then(function(response){
            vm.companySuggestion = response.data;
            vm.formdata.symbol = "";
            $scope.dropdown.search = true;
        });
      } else {
        vm.formdata.symbol = "";
        vm.companySuggestion = [];
      }
    }

    function add_stock(){
      if (vm.formdata.company_name.length > 1){
        Layout.add_stock(vm.formdata).then(function successCallback(response){
          vm.show_alert(" Stock added in your portfolio", "success");
          vm.clearSelected();
          vm.get_stocks();
        }, function failureCallback(response){
          if (response.status == 400) {
            if (response.data.symbol != null) {
              msg = response.data.symbol[0];
              vm.show_alert(msg,"failure");
            };
          };
        });
      } else {
        vm.show_alert(" No Company is listed with given Symbol", "failure");
      }
    }

    function add_watch_stock(){
      if (vm.formdata.company_name.length > 1){
        Layout.add_watch_stock(vm.formdata).then(function successCallback(response){
          vm.show_alert(" Stock added in your Watch List", "success");
          vm.clearSelected();
          vm.get_watchlist();
        }, function failureCallback(response){
          if (response.status == 400) {
            if (response.data.symbol != null) {
              msg = response.data.symbol[0];
              vm.show_alert(msg,"failure");
            };
          };
        });
      } else {
        vm.show_alert(" No Company is listed with given Symbol", "failure");
      }
    }
    function addToExisting(){
      
      vm.formdata.invested_price = Math.ceil((vm.selected_stock.invested_amount + 
        vm.formdata.N_stocks*vm.formdata.invested_price )/(vm.formdata.N_stocks+
        vm.selected_stock.N_stocks)*100)/100;
      vm.formdata.N_stocks += vm.selected_stock.N_stocks;
      vm.formdata.symbol = vm.selected_stock.symbol;
      vm.formdata.company_name = vm.selected_stock.companyName;
      vm.formdata.target_price = vm.selected_stock.target_price;
      vm.formdata.trigger_price_high = vm.selected_stock.trigger_price_high;
      vm.formdata.trigger_price_low = vm.selected_stock.trigger_price_low;

      id = vm.selected_stock.id;
      
      Layout.edit_stock(id, vm.formdata)
      .then(function successCallback(response){
        vm.show_alert(" Stock added in your portfolio", "success");
        vm.clearSelected();
        vm.get_stocks();
      }, function failureCallback(response){
        vm.show_alert("Error Occured!","failure");
      });
    }

    function editStock(){
      vm.selected_stock['company_name'] = vm.selected_stock['companyName'];

      Layout.edit_stock(vm.selected_stock.id , vm.selected_stock)
      .then(function successCallback(response){
        vm.show_alert(" Stock values updated", "success");
        vm.clearSelected();
        vm.get_stocks();
      }, function failureCallback(response){
        vm.show_alert("Error Occured!","failure");
      });
    }
    function sellStock(){
      
      vm.formdata.invested_price = vm.selected_stock.invested_price;
      vm.profit = Math.ceil((vm.formdata.selling_price -  vm.formdata.invested_price)*vm.formdata.N_stocks*0.993);
      vm.formdata.N_stocks = vm.selected_stock.N_stocks - vm.formdata.N_stocks;
      vm.formdata.symbol = vm.selected_stock.symbol;
      vm.formdata.company_name = vm.selected_stock.companyName;
      vm.formdata.target_price = vm.selected_stock.target_price;
      vm.formdata.trigger_price_high = vm.selected_stock.trigger_price_high;
      vm.formdata.trigger_price_low = vm.selected_stock.trigger_price_low;
      id = vm.selected_stock.id;
      
      Layout.edit_stock(id, vm.formdata)
      .then(function successCallback(response){
        vm.show_alert(" Stock sold from your portfolio, Profit is " + vm.profit.toString(), "success");
        vm.clearSelected();
        vm.get_stocks();
      }, function failureCallback(response){
        vm.show_alert("Error Occured!","failure");
      });
    }
    function editStockWatchList(){

      vm.selected_stock['company_name'] = vm.selected_stock['companyName'];

      Layout.edit_stock_watch_list(vm.selected_stock.id , vm.selected_stock)
      .then(function successCallback(response){
        vm.show_alert(" Stock values updated", "success");
        vm.clearSelected();
        vm.get_watchlist();
      }, function failureCallback(response){
        vm.show_alert("Error Occured!","failure");
      });
    }
    function delete_stock(){
      Layout.delete_stock(vm.selected_stock.id)
      .then(function(response){
        vm.show_alert("Stock is deleted!","success");
        vm.get_stocks();
        vm.clearSelected();
      });
    }
    function delete_stock_watch_list(){
      Layout.delete_stock_watch_list(vm.selected_stock.id)
      .then(function(response){
        vm.show_alert("Stock is deleted!","success");
        vm.get_watchlist();
        vm.clearSelected();
      });
    }
    function showSearchSuggetsion() {
      return (vm.companySuggestion.length > 0) && vm.formdata.symbol.length == 0 && $scope.dropdown.search
    }
    function createRefreshOptionList(){
      for (var i = 0; i < vm.refreshOption.length; i++) {
        if (vm.refreshOption[i] >= 60) {
          vm.refreshOptionList.push({"time": (vm.refreshOption[i]/60).toString() + " minutes","id": i });
        } else {
          vm.refreshOptionList.push({"time": vm.refreshOption[i].toString() + " seconds","id": i });
        }
      };
    }
    function clearSelected(){
      vm.selected_stock = {};
      vm.formdata = {};
      vm.formdata.symbol = "";
      vm.formdata.company_name = "";
      vm.stock_operation = "";
      vm.watchlist_operation = "";
    }
    function selectCompany(item){
      vm.formdata.symbol = item.symbol;
      vm.formdata.company_name = item.name;
      vm.companySuggestion = [];
    }
    function alert(msg,type){

      vm.alert.message = msg;

      if (type == "success") {
        vm.alert.success = true;
      } else if(type == "failure"){
        vm.alert.failure = true;
      }
      $timeout(function() {
        if (type == "success") {
          vm.alert.success = false;
        } else if(type == "failure"){
          vm.alert.failure = false;
        }
      }, 3000);
    }
    function duringExhangeOpen(){
      var date = new Date();
      if (date.getHours() > 8 && date.getHours() < 17) {
        vm.get_stocks();
        vm.get_watchlist();
      };
    }
    function refresh(){
      vm.get_stocks();
      vm.get_watchlist();
    }
    function get_watchlist(){
      vm.process.updating = true;
      Layout.get_stocks_watch()
      .then(function(response){

        if (response.data !== null) {
          vm.stocksWatchList = response.data;
          vm.date = Date.now();
          // Notification system
          vm.notification_text_high = ""
          vm.notification_text_low = ""
          if (vm.stocksWatchList.length > 0) {
          
            if (Notification.permission == "granted") {

              for (var i = vm.stocksWatchList.length - 1; i >= 0; i--) {
                if(vm.stocksWatchList[i].trigger_price_high < vm.stocksWatchList[i].lastPrice){
                  vm.notification_text_high += vm.stocksWatchList[i].symbol + "\n";
                }
                if(vm.stocksWatchList[i].trigger_price_low > vm.stocksWatchList[i].lastPrice){
                  vm.notification_text_low += vm.stocksWatchList[i].symbol + "\n";
                }
              };
              if(vm.notification_text_high.length > 1){
                var notification = new Notification('Sell', {
                  icon: 'http://www.iconsdb.com/icons/preview/soylent-red/sell-2-xxl.png',
                  body: vm.notification_text_high,
                });
              }
              if(vm.notification_text_low.length > 1){
                var notification = new Notification('Buy', {
                  icon: 'https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/shopping-circle-green-128.png',
                  body: vm.notification_text_low,
                });
              }
            };
          };
        };
      });
    }
    function get_stocks(){
      vm.process.updating = true;
      Layout.get_stocks()
      .then(function(response){

      if (response.data !== null) {
        vm.stocksList = response.data;
        // Calculate portfolio change
        vm.portfolio.change = 0;
        vm.portfolio.invested_amount = 0;
        vm.portfolio.percent_change = 0;
        vm.portfolio.daily_change = 0;
        vm.portfolio.daily_change_percent = 0;
        vm.portfolio.latestValue = 0;


        for (var i = vm.stocksList.length - 1; i >= 0; i--) {
          vm.portfolio.invested_amount += vm.stocksList[i].invested_amount;
          vm.portfolio.daily_change += vm.stocksList[i].daily_amount_change;
          vm.portfolio.latestValue += vm.stocksList[i].latest_value;
        };
        vm.portfolio.change = vm.portfolio.latestValue - vm.portfolio.invested_amount
        vm.portfolio.percent_change = vm.portfolio.change/vm.portfolio.invested_amount*100;
        vm.portfolio.daily_change_percent = vm.portfolio.daily_change/vm.portfolio.invested_amount*100;
        $rootScope.portfolio_change = Math.ceil(vm.portfolio.daily_change).toString() + "/" + Math.ceil(vm.portfolio.change).toString();
        vm.showpage = true;
        vm.process.updating = false;
        vm.date = Date.now();
        // Notification system
        vm.notification_text_high = ""
        vm.notification_text_low = ""
        if (vm.stocksList.length > 0) {
        
          if (Notification.permission == "granted") {

            for (var i = vm.stocksList.length - 1; i >= 0; i--) {
              if(vm.stocksList[i].trigger_price_high < vm.stocksList[i].lastPrice){
                vm.notification_text_high += vm.stocksList[i].symbol + " " + vm.stocksList[i].lastPrice.toString()
                  + "/" + vm.stocksList[i].invested_price + "\n";
              }
              if(vm.stocksList[i].trigger_price_low > vm.stocksList[i].lastPrice){
                vm.notification_text_low += vm.stocksList[i].symbol + " " + vm.stocksList[i].lastPrice.toString()
                  + "/" + vm.stocksList[i].invested_price + "\n";
              }
            };
            if(vm.notification_text_high.length > 1){
              var notification = new Notification('Sell', {
                icon: 'http://www.iconsdb.com/icons/preview/soylent-red/sell-2-xxl.png',
                body: vm.notification_text_high,
              });
            }
            if(vm.notification_text_low.length > 1){
              var notification = new Notification('Buy', {
                icon: 'https://cdn0.iconfinder.com/data/icons/social-messaging-ui-color-shapes/128/shopping-circle-green-128.png',
                body: vm.notification_text_low,
              });
            }
          };
        };
      };
      });
    }
  };
})();