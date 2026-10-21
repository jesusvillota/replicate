jQuery(document).ready(function ($) {
  ppd_init($);
  scrollToHash();
});

function scrollToHash() {
  var hash = window.location.hash;
  if (hash) {
    var element = document.getElementById(hash.substring(1));
    if (element) {
      element.scrollIntoView({ behavior: "smooth" });
    }
  }
}

function ppd_init($) {
  $(".expandable").gnReadMore({ height: 45 });

  $("input").on("focus", function () {
    if ($(this).val() == $(this).data("default-value")) {
      $(this).val("");
    }
  });

  $("input").on("blur", function () {
    if ($(this).val() == "") {
      $(this).val($(this).data("default-value"));
    }
  });

  $("textarea").on("focus", function () {
    if ($(this).val() == $(this).data("default-value")) {
      $(this).val("");
    }
  });

  $("textarea").on("blur", function () {
    if ($(this).val() == "") {
      $(this).val($(this).data("default-value"));
    }
  });

  init_documentation($);

  init_slideshow($);

  init_nav_indicator($);

  init_data_browser($);

  $(".ppd-column-name").hover(
    function () {
      $(this).data("title", $(this).attr("title"));
      $(this).removeAttr("title");
    },
    function () {
      $(this).attr("title", $(this).data("title"));
    }
  );

  // responsive menu
  $("#access ul li.toggle").click(function () {
    $(this).parent().toggleClass("open");
  });

  //Download links

  function postURL(url, postargs) {
    $form = $(
      "<form action='" + url + "' xtarget='_blank' method='post'></form>"
    );
    for (var key in postargs) {
      if (postargs.hasOwnProperty(key)) {
        $form.append(
          '<input type="hidden" name="' +
          key +
          '" value="' +
          postargs[key] +
          '"/>'
        );
      }
    }
    $("body").append($form);
    $form.submit();
    //$form.remove();
  }

  /* To delete:
  source_PlanBasics
-InPFS
-source_GASBAssumptions
-source_FundingAndMethods
-source_GASBSchedules
-source_InvestmentReturn
-source_IncomeStatement
-source_ActCosts
-source_membership
-source_ActLiabilities
*/

  function downloadData(version, filename) {
    var postargs = [];
    postargs["a"] = "data-download";
    postargs["q"] = "QVariables";
    postargs["variables"] =
      "ppd_id,PlanName,fy,system_id,PlanFullName,source_PlanBasics,FiscalYearType,PlanInceptionYear,PlanClosed,PlanYearClosed,AdministeringGovt,StateAbbrev,StateName,GovtName,PlanType,EmployeeTypeCovered,SocSecCovered,SocSecCovered_verbatim,CostStructure,EmployerType,CostSharing,BenefitsWebsite,EEGroupID,TierID,ActRptDate,fye,ActCostMeth_GASB,AssetValMeth_GASB,FundingMeth_GASB,InflationAssumption_GASB,InvestmentReturnAssumption_GASB,ActCostMethCode_GASB,AssetValMethCode_GASB,AssetSmoothingPeriod_GASB,FundingMethCode1_GASB,FundingMethCode2_GASB,UAALAmortPeriod_GASB,BlendedDiscountRate,AssetValMeth,PhaseIn,AssetValMeth_note,ActCostMeth,ActCostMeth_note,FundingMeth,FundingMeth_note,MktAssets_Smooth,ActAssets_Smooth,NetFlows_smooth,AssetValMethCode,SmoothingReset,GainlossConcept,GainLossBase_1,GainLossBase_2,GainLoss,GainLossPeriod,PhaseInPercent,PhaseInPeriods,PhaseInType,GainLossRecognition,AssetSmoothingBaseline,ExpectedReturnMethod,AddSubtractGainLoss,UpperCorridor,LowerCorridor,ActCostMethCode,FundMethCode_1,FundMethCode_2,PayrollGrowthAssumption,TotAmortPeriod,RemainingAmortPeriod,UAALYearEstablished,WageInflation,ActAssets_GASB,ActLiabilities_GASB,ActFundedRatio_GASB,UAAL_GASB,ActLiabilities_other,payroll,RequiredContribution,PercentReqContPaid,TotalPensionLiability,NetPosition,NetPensionLiability,ActAssets_est,ActLiabilities_est,ActFundedRatio_est,RequiredContribution_est,ActFundedRatio_GASB67,InvestmentConsultantName,InvestmentConsultantCode,InvestmentReturn_1yr,InvestmentReturn_2yr,InvestmentReturn_3yr,InvestmentReturn_4yr,InvestmentReturn_5yr,InvestmentReturn_7yr,InvestmentReturn_8yr,InvestmentReturn_10yr,InvestmentReturn_12yr,InvestmentReturn_15yr,InvestmentReturn_20yr,InvestmentReturn_25yr,InvestmentReturn_30yr,InvestmentReturn_LongTerm,InvestmentReturn_LTStartYear,GrossReturns,GeoReturn_est,GeoGrowth_est,InvestmentReturn_1yr_est,InvestmentReturn_5yr_est,InvestmentReturn_10yr_est,AvgReturn_3yr,AvgReturn_5yr,AvgReturn_10yr,expense_SecLendMgmtFees,contrib_EE_regular,contrib_ER_regular,contrib_ER_state,contrib_EE_PurchaseService,contrib_EE_other,contrib_ER_other,contrib_other,POB_Flag,POB_Amount,contrib_tot,FairValueChange_investments,FairValueChange_RealEstate,income_interest,income_dividends,income_InterestAndDividends,income_RealEstate,income_PrivateEquity,income_alternatives,income_international,income_OtherInvestments,expense_RealEstate,expense_PrivateEquity,expense_alternatives,expense_OtherInvestments,expense_investments,FVChange_SecLend,income_SecuritiesLending,expense_SecuritiesLending,income_SecuritiesLendingRebate,FVChange_SecLend_UG,income_OtherAdditions,income_net,expense_TotBenefits,expense_RetBenefits,expense_DisabilityBenefits,expense_DeathBenefits,expense_DROPBenefits,expense_SurvivorBenefits,expense_COLABenefits,expense_LumpSumBenefits,expense_OtherBenefits,expense_refunds,expense_AdminExpenses,expense_Depreciation,expense_OtherDeductions,expense_net,adjustment_MktAssets,MktAssets_net,BegMktAssets_net,contrib_ER_tot,contrib_other_tot,FairValueChange_tot,income_interest_dividends_tot,expense_investments_tot,SecLend_tot,investments_net,expense_other_tot,ContributionFY,ActuarialFirm,ActuarialFirmCode,NormCostRate_tot,NormCostRate_EE,NormCostRate_ER,ReqContRate_ER,ReqContRate_tot,ReqContRate_ER_Stat,ReqContRate_tot_Stat,NormCostAmount_tot,NormCostAmount_EE,NormCostAmount_ER,ReqContAmount_ER,ReqContAmount_tot,ReqContAmount_ER_Stat,ReqContAmount_tot_Stat,NormCostRate_tot_est,NormCostRate_EE_est,NormCostRate_ER_est,ReqContRate_ER_est,ProjectedPayroll,UAALRate,beneficiaries_DisabilityRetirees,beneficiaries_DependentSurvivors,actives_tot,ActiveSalaries,ActiveAge_avg,ActiveTenure_avg,ActiveSalary_avg,InactiveVestedMembers,InactiveNonVested,beneficiaries_tot,benefits_tot,BeneficiaryAge_avg,BeneficiaryBenefit_avg,beneficiaries_ServiceRetirees,benefits_ServiceRetirees,ServiceRetireeAge_avg,ServiceRetireeBenefit_avg,ServiceRetAge_avg,ServiceRetTenure_avg,benefits_DisabilityRetirees,beneficiaries_survivors,beneficiaries_SpousalSurvivors,beneficiaries_other,DROPMembers,OtherMembers,TotMembership,ActiveSalary_avg_est,BeneficiaryBenefit_avg_est,PVFB_InactiveNonVested,PVFB_active,PVFB_InactiveVested,PVFB_retiree,PVFB_other,PVFB_tot,PVFNC_tot,PVFC_EE,PVFNC_ER,PVFS,AccruedLiab_active,PVFC_tot,PVFC_ER,ActAssets_BalSht,TotFund_BnchmrkRtrn,Leverage_Flag,Leverage_Total_Actl,Leverage_Total_Trgt,EQTotal_Rtrn,EQTotal_Actl,EQTotal_Trgt,FITotal_Rtrn,FITotal_Actl,FITotal_Trgt,RETotal_Rtrn,RETotal_Actl,RETotal_Trgt,AltMiscTotal_Rtrn,AltMiscTotal_Actl,AltMiscTotal_Trgt,PETotal_Rtrn,PETotal_Actl,PETotal_Trgt,HFTotal_Rtrn,HFTotal_Actl,HFTotal_Trgt,COMDTotal_Rtrn,COMDTotal_Actl,COMDTotal_Trgt,CashTotal_Rtrn,CashTotal_Actl,CashTotal_Trgt,OtherTotal_Rtrn,OtherTotal_Actl,OtherTotal_Trgt,Duration_Type,Duration_describe,Total_Duration,Total_MktVal_Duration";
    postargs["filtereegroupid"] = 0;
    postargs["filtertierid"] = 0;
    if (version) {
      postargs["version"] = version;
    }
    postargs["filename"] = filename;

    postargs["format"] = "csv";

    //postURL('https://publicplansdata.org/api/',postargs);
    postURL("/api/", postargs);
  }

  $("a.ppd-download").click(function (event) {
    event.preventDefault();
    var el = this;
    var version = $(el).data("ppd-version");
    var filename = $(el).data("ppd-filename");

    // Optionally, set a data attribute for tracking
    $(el).attr("data-version", version);
    $(el).attr("data-filename", filename);

    gnClickTrack(el, function () {
      // This runs after tracking (and after the dialog, if needed)
      downloadData(version, filename);
    });
  });
}

function stripTableIDs(strArray) {
  replacementArray = new Array();
  strArray.forEach(function (element) {
    replacementArray.push(stripTableID(element));
  });
  return replacementArray;
}
function stripTableID(str) {
  return str.replace(/_\d+$/, "");
}
function array_unique(array) {
  return array.filter(function (el, index, arr) {
    return index == arr.indexOf(el);
  });
}

function QueryStringToJSON(str) {
  str = decodeURI(str);
  var pairs = str.split("&");
  var result = {};
  pairs.forEach(function (pair) {
    pair = pair.split("=");
    var name = pair[0];
    var value = pair[1];
    if (name.length)
      if (result[name] !== undefined) {
        if (!result[name].push) {
          result[name] = [result[name]];
        }
        result[name].push(value || "");
      } else {
        result[name] = value || "";
      }
  });
  return result;
}

function arrayToTable(tableData, dataKeys) {
  var table = $('<table class="tablesorter"></table>');

  var headerRow = $("<tr></tr>");
  $(dataKeys).each(function (i, key) {
    $(headerRow).append($("<th>" + key + "</th>"));
  });

  //

  var thead = $("<thead></thead>");

  thead.append(headerRow);
  table.append(thead);

  /*
  var headerRow = $('<tr></tr>');

  $(dataKeys).each(function (i, key) {
        $(headerRow).append($('<th>'+key+'</th>'));
        });

  $(thead).append (headerRow);

    $( table).append(thead);
*/
  //
  //table.append(headerRow);

  $(tableData).each(function (i, rowData) {
    var row = $("<tr></tr>");
    $(dataKeys).each(function (j, key) {
      row.append($("<td>" + rowData[key] + "</td>"));
    });
    table.append(row);
  });
  return table;
}

function getAPIQuery(format) {
  var searchInput = QueryStringToJSON(jQuery("#ppd-search").serialize());

  if (searchInput["ppd_id[]"] && !Array.isArray(searchInput["ppd_id[]"])) {
    searchInput["ppd_id[]"] = new Array(searchInput["ppd_id[]"]);
  }

  var cols = searchInput["cols[]"];
  //cols = array_unique(stripTableIDs(cols));
  cols = array_unique(cols);

  var url =
    "/api/?a=interactivebrowser&q=QVariables&format=" +
    format +
    "&filtereegroupid=0&variables=" +
    cols.join(",");

  if (searchInput["ppd-null-to-zero"]) {
    url += "&null2zero=1";
  }
  if (searchInput["ppd_id[]"]) {
    url += "&filterppdid=" + searchInput["ppd_id[]"].join(",");
  }

  url +=
    "&filterfystart=" + (searchInput["fy_s"] ? searchInput["fy_s"] : "1995");
  url +=
    "&filterfyend=" +
    (searchInput["fy_e"] ? searchInput["fy_e"] : new Date().getFullYear());

  delete searchInput["cols[]"];
  delete searchInput["ppd_id[]"];
  delete searchInput["ppd-null-to-zero"];
  delete searchInput["fy_s"];
  delete searchInput["fy_e"];

  var old_params = jQuery.param(searchInput);

  if (old_params) {
    url += "&" + old_params.toLowerCase();
  }

  return url;
}
function filterFilterValue(str) {
  str = str.replace(/\|/g, " or ");
  return str;
}
function getDynamicFilters() {
  var filters = new Array();
  var $ = jQuery;
  // Loop over filter elements; if not blank; grab variable name, filter value, and add to ffilter
  $("#ppd-query-result th").each(function (index, item) {
    var col = $(this).data("column");
    var value = "";
    if (
      (value = $("input.tablesorter-filter[data-column=" + col + "]").val()) !=
      ""
    ) {
      filters.push(
        $(item).data("ppd-variable") + "," + filterFilterValue(value)
      );
    }
  });

  var filterString = filters.join("|");

  if (filterString) {
    filterString = "&ffilter=" + filterString;
  }

  return filterString;
}

function init_data_browser($) {
  var w = $(window).width();
  var h = $(window).height();

  $(".gn-data-dialog").dialog({
    height: h,
    zIndex: 10,
    autoOpen: false,
    modal: true,
    resizable: true,
    width: w,
  });



  $(".gn-download-data").click(function (e) {
    e.preventDefault(); // Prevent default navigation for now
    var apiQuery = getAPIQuery("csv");
    apiQuery += "&null2zero=1";
    var finalUrl = apiQuery + "&filename=ppd-query";
    console.log("Chris says: in gn-download-data. Final URL is: " + finalUrl);

    // Set the data-url attribute so the tracker can pick it up
    $(this).attr("data-url", finalUrl);
    // Call tracking, then proceed with your logic
    gnClickTrack(this, function () {
      document.location = finalUrl
    });
    return false;

    // var apiQuery = getAPIQuery("csv");
    // apiQuery += "&null2zero=1";
    // document.location = apiQuery + "&filename=ppd-query";
    // return false;
  });

  $("body").on("click", ".ppd-filtered-download-data", function (item) {
    var apiQuery = getAPIQuery("csv");
    apiQuery += "&null2zero=1";
    apiQuery += "&filename=ppd-query";
    apiQuery += getDynamicFilters();

    $(this).attr("href", apiQuery);
    return true;
  });

  $(".gn-open-databrowser").click(function () {
    //Reset top

    $("html").scrollTop(0);
    var dialogID = $(this).data("dialog");
    var $dialog = $("#" + dialogID);

    var apiQuery = getAPIQuery("html");

    $dialog.html(
      "<div style='height:100%; max-width:100%;'><img style='margin-top:25%;margin-left:50%; margin-right:auto;' src='/wp-admin/images/loading.gif'/></div>"
    );
    $dialog.dialog("open").addClass("ppd-data-browser");

    $(".ppd-data-browser").css("min-height", $("html").height());
    /*
      $(".ppd-data-browser").css("min-width","100%");
      */

    //$dialog.closest('.ui-dialog').css("min-height",$("html").height());
    $dialog.closest(".ui-dialog").css("min-width", "100%");

    //Full Dialog
    $("#ppd-search-results-dialog").css("overflow-y", "visible");
    $("#ppd-search-results-dialog").css("height", "90%");
    $("div.ui-dialog").height("100%");
    //$("div.ui-dialog").css("overflow-y","hidden")

    $.get(apiQuery, function (response, textStatus, jqXHR) {
      //surveyOnLoad($dialog);
      //$dialog.html(arrayToTable(response.slice(1), cols));

      $downloadLink =
        '<p class="ppd-csv-link"><a class="ppd-filtered-download-data" href="#" target="_blank">Download filtered data as CSV</a></p>';

      $dialog.html(response + $downloadLink);
      $dialog.find("table").wrap("<div id='ppd-query-result'></div>");
      $dialog.find("table").each(function () {
        makeTableSorter.call(this, $).bind("filterEnd", function (e, table) {
          resizeInteractiveBrowserResults();
        });
      });
      //Full Dialog
      $("#ppd-search-results-dialog").css("overflow-y", "visible");

      $dialog.closest(".ui-dialog").css("min-width", "100%");
      $dialog.closest(".ui-dialog").css("width", "auto");

      // Fix top for scrolling/
      $(".ui-dialog-titlebar").css("position", "fixed");
      $(".ui-dialog-titlebar").css("width", "100%");
      $(".ui-dialog-titlebar").css("top", "0");
      $(".ui-dialog-titlebar").css("z-index", "1");

      // Margin for the fixed dialog bar above
      $("#ppd-search-results-dialog").css("margin-top", "34px");

      $("#ppd-search-results-dialog").css("height", "auto");
      $("#ppd-search-results-dialog").css("width", "auto");
      $dialog
        .closest("div.ui-dialog")
        .height($("#ppd-search-results-dialog").height() + 40);
      $dialog.closest("div.ui-dialog").css("overflow-y", "hidden");

      //Zebra + Filter
      $("#ppd-search-results-dialog table").trigger("applyWidgets");
      // Filter hints
      $("#ppd-search-results-dialog .tablesorter-filter-row input").attr(
        "title",
        "(e.g. 2013, < 5, > 5, TX); separate discrete values with | (e.g.,  TX|AL)"
      );
    });

    return false;
  });
}

function resizeInteractiveBrowserResults() {
  var $ = jQuery;
  $("div.ui-dialog").height($("#ppd-search-results-dialog").height() + 40);
}

function init_nav_indicator($) {
  $("#access .menu-header .menu-item a").append(
    '<div class="nav-indicator clearfix"><div class="nav-indicator-back"></div><div class="nav-indicator-front"></div></div>'
  );

  $("#access .nav-indicator").css("paddingLeft", function () {
    var wid = $(this).css("width");
    wid = wid.replace("px", "");
    wid = parseInt(wid);
    wid = wid - 19;
    wid = wid / 2;
    return wid;
  });

  $(
    "#access .current-menu-item .nav-indicator-front, #access .current-menu-ancestor .nav-indicator-front, #access .current-page-ancestor .nav-indicator-front"
  ).css("backgroundPositionY", "0");
  $(
    "#access .current-menu-item .nav-indicator-back, #access .current-menu-ancestor .nav-indicator-back, #access .current-page-ancestor .nav-indicator-back"
  ).css("backgroundPositionY", "0");

  var menuItem;
  var menuItemFront;
  var menuItemBack;

  $("#access .menu-item").hover(
    function () {
      menuItem = $(this).attr("class");
      menuItem = menuItem.replace(/\s+/g, ".");
      menuItem = "." + menuItem;
      menuItemBack = menuItem + " .nav-indicator-back";
      menuItemFront = menuItem + " .nav-indicator-front";

      menuItemBackPos = $(menuItemBack).css("backgroundPosition");

      if (
        $(menuItem).hasClass("current-menu-item") ||
        $(menuItem).hasClass("current-menu-ancestor") ||
        $(menuItem).hasClass("current-page-ancestor")
      ) {
        $(menuItemBack).css("backgroundPositionY", "0");
        $(menuItemFront).css("backgroundPositionY", "0");
      } else {
        $(menuItemBack).animate({ backgroundPositionY: "0px" }, 200);
        $(menuItemFront)
          .delay(100)
          .animate({ backgroundPositionY: "0px" }, 200);
      }
    },
    function () {
      if (
        $(menuItem).hasClass("current-menu-item") ||
        $(menuItem).hasClass("current-menu-ancestor") ||
        $(menuItem).hasClass("current-page-ancestor")
      ) {
        $(menuItemBack).css("backgroundPositionY", "0");
        $(menuItemFront).css("backgroundPositionY", "0");
      } else {
        $(menuItemFront).animate({ backgroundPositionY: "-25px" }, 200);
        $(menuItemBack).delay(100).animate({ backgroundPositionY: "5px" }, 100);
      }
    }
  );
}

function scrollToElement($scrollTo, $container) {
  var offset =
    $scrollTo.offset().top - $container.offset().top + $container.scrollTop();
  $container.animate({ scrollTop: offset }, 500);
}

function init_documentation($) {
  var $container = $("#pubplans-tables");

  function collapseAll() {
    $(".ppd-tabletoggle.expanded").toggleClass("expanded collapsed");
    $(".pubplans-tablecols").hide();
  }

  $("#pubplans-tableselect").change(function () {
    collapseAll();
    // location.hash = $(this).val();
    var $scrollTo = $("#ppd-" + $(this).val());
    scrollToElement($scrollTo, $container);
    $scrollTo.find(".ppd-tabletoggle.collapsed").click();
  });

  /*
  if(location.hash && $container.length) {
    var key = location.hash.substr(1);
    var $scrollTo = $("#ppd-"+key);
    $("#pubplans-tableselect").val(key);
    scrollToElement ($scrollTo, $container);
    $scrollTo.find(".ppd-tabletoggle.collapsed").click();
  }
  */

  $(".ppd-tabletoggle").click(function (e) {
    if (e.target == this) {
      $(this).toggleClass("expanded collapsed");
      $(this).attr("title", $(this).hasClass("collapsed") ? "Show" : "Hide");
      $(this).next(".pubplans-tablecols").toggle(500);
      $(this).children(".pubplans-tablecols").toggle(500);
    }
  });
}

function init_slideshow($) {
  $("#feature")
    .after('<div id="nav" class="clearfix">')
    .cycle({
      fx: "scrollHorz",
      speed: 500,
      timeout: 10000,
      pager: "#nav",
      cleartypeNoBg: true,
      pagerAnchorBuilder: function (idx, slide) {
        return '<div class="circle left"><a href="#"></a></div>';
      },
    });

  /*
  $(".header-images.left").each(function (idx) {
    var delay = [2000, 4000, 0];
    var cycleOptions = {
      fx: 'fade',
      speed: 4000,
      timeout: 10000,
      delay: delay[idx]
    };

    $(this).cycle(cycleOptions);
  });
  */
}

//2020

jQuery(document).ready(function ($) {
  jQuery(".add-see-more").each(function (index) {
    var content = $(".add-see-more").html();
    var href = $(".add-see-more").parent("a").attr("href");
    var target = $(".add-see-more").parent("a").attr("target");

    $(this).replaceWith(
      "<div class='see-more weird clearfix'><a href='" +
      href +
      "' target='" +
      target +
      "'><h5 class='left'>" +
      content +
      "</h5><div class='arrow green left'></div></a></div>"
    );
  });
});

jQuery(document).ready(function ($) {
  $("#pitDialog").hide();
  $("#pitDialog").load("/tools/pensioninvestments/", function () {
    $("#pitDialog").dialog({
      position: { my: "top", at: "top", of: window },
      width: "100%",
      left: 0,
      height: "auto",
      minHeight: 1000,
      autoOpen: false,
      modal: true,
      dialogClass: "crrPensionInvestmentToolDialog",
    });

    $("#pitTool,.pitTool").click(function () {
      $("html").scrollTop(0);
      $("#pitDialog").dialog("open");
      $("#pitDialog").dialog({
        position: { my: "top", at: "top", of: window },
      });
      return false;
    });
  });
});

jQuery(document).ready(function ($) {
  $("body").on("click", ".code-copy", function () {
    $(this).prev("textarea").select();
    document.execCommand("copy");
  });
});

function survey_2021_no_more() {
  //Cookies.set("ppd_survey_2021_blocked", "true", { expires: 365 });
  document.cookie = "ppd_survey_2021_blocked=true; expires=Fri, 09 Mar 2027 00:00:00 UTC; path=/";
}
