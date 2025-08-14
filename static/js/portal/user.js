function generateDatatable() {
    $('#generalTotalTable').kendoGrid({
            dataSource: {
                transport: {
                    read: {
                        url: "/kendo/?slug=vatandas",
                        type: "POST",
                        headers: token,
                    },
                    dataType: "jsonp",
                },
                schema: {
                    data: "results",
                    total: "count",
                },
                filter: {
                    filters: [{field: 'activities__id__in', operator: 'eq', value: activityId}]
                },
                pageSize: 7,
                serverPaging: true,
                serverFiltering: true,
                serverSorting: true
            },
            dataBound: () => {
                $('.get_tc_info_btn').click(function() {
                    getCitizenInfo(this.dataset.tc)
                });
            },
            pageable: {
                refresh: true,
                pageSizes: true,
            },
            height: 730,
            filterable: {
                mode: "row"
            },
            sortable: false,
            columns: [
                {
                    field: "isim",
                    title: "Ad",
                    filterable: {
                        cell: {
                            operator: "contains",
                            suggestionOperator: false,
                            template: function (e) {
                                e.element.kendoAutoComplete({
                                    serverFiltering: false,
                                    valuePrimitive: true,
                                    noDataTemplate: ''
                                });
                            }
                        }
                    },
                    template: function (params) {
                        return params.isim.charAt(0).toUpperCase() + params.isim.slice(1);
                    },
                    width: 200
                },{
                    field: "soyisim",
                    title: "Soyad",
                    filterable: {
                        cell: {
                            operator: "contains",
                            suggestionOperator: false,
                            template: function (e) {
                                e.element.kendoAutoComplete({
                                    serverFiltering: false,
                                    valuePrimitive: true,
                                    noDataTemplate: ''
                                });
                            }
                        }
                    },
                    width: 200,
                    template: function (params) {
                        return params.soyisim.charAt(0).toUpperCase() + params.soyisim.slice(1);
                    }
                },{
                    field: "tckn",
                    title: "TC Kimlik",
                    width: 150,
                    filterable: {
                        cell: {
                            operator: "exact",
                            suggestionOperator: false,
                            template: function (e) {
                                e.element.kendoAutoComplete({
                                    serverFiltering: false,
                                    valuePrimitive: true,
                                    noDataTemplate: ''
                                });
                            }
                        }
                    }
                },{
                    field: "egitim_durumu",
                    title: "Eğitim Durumu",
                    filterable: {
                        cell: {
                            operator: "eq",
                            showOperators: false,
                            template: function(args) {
                                args.element.kendoDropDownList({
                                dataSource: ["Okul Öncesi", "İlkokul", "Ortaokul", "Lise", "Ön Lisans", "Lisans", "Yüksek Lisans", "Doktora"],
                                optionLabel: "--Seçiniz--"
                                });
                            }
                        }
                    },
                    width: 200
                },{
                    field: "yas",
                    title: "Yaş",
                    filterable: {
                        cell: {
                            operator: "exact",
                            suggestionOperator: false,
                            template: function (e) {
                                e.element.kendoAutoComplete({
                                    serverFiltering: false,
                                    valuePrimitive: true,
                                    noDataTemplate: ''
                                });
                            }
                        }
                    },
                    width: 100
                }, {
                    field: "nvi_ilce",
                    title: "İlçe",
                    filterable: {
                        cell: {
                            operator: "contains",
                            showOperators: false,
                            template: function(args) {
                                args.element.kendoDropDownList({
                                dataSource: ["ADALAR", "ARNAVUTKÖY", "ATAŞEHİR", "AVCILAR", "BAĞCILAR", "BAHÇELİEVLER",
                                    "BAKIRKÖY", "BAŞAKŞEHİR", "BAYRAMPAŞA", "BEŞİKTAŞ", "BEYKOZ", "BEYLİKDÜZÜ", "BEYOĞLU",
                                    "BÜYÜKÇEKMECE", "ÇATALCA", "ÇEKMEKÖY", "ESENLER", "ESENYURT", "EYÜPSULTAN", "FATİH",
                                    "GAZİOSMANPAŞA", "GÜNGÖREN", "KADIKÖY", "KADIKÖY", "KAĞITHANE", "KARTAL",
                                    "KÜÇÜKÇEKMECE", "MALTEPE", "PENDİK", "SANCAKTEPE", "SARIYER", "SİLİVRİ", "SULTANBEYLİ",
                                    "SULTANGAZİ", "ŞİLE", "ŞİŞLİ", "TUZLA", "ÜMRANİYE", "ÜSKÜDAR", "ZEYTİNBURNU"],
                                optionLabel: "--Seçiniz--"
                                });
                            }
                        }
                    },
                    width: 200
                }, {
                    field: "nvi_mahalle",
                    title: "Mahalle",
                    filterable: {
                        cell: {
                            operator: "contains",
                            suggestionOperator: false,
                            template: function (e) {
                                e.element.kendoAutoComplete({
                                    serverFiltering: false,
                                    valuePrimitive: true,
                                    noDataTemplate: ''
                                });
                            }
                        }
                    },
                    template: function (params) {
                        return params.nvi_mahalle
                            ? params.nvi_mahalle.charAt(0).toUpperCase() + params.nvi_mahalle.slice(1)
                            : '';
                    },
                    width: 200
                }, {
                    template: `<a class="btn btn-icon btn-light-twitter me-5 get_tc_info_btn" data-tc="#:tckn#"><i class="fas fa-info"></i></a>`,
                    title: "",
                    width: 80
                }
            ]
        });
    }