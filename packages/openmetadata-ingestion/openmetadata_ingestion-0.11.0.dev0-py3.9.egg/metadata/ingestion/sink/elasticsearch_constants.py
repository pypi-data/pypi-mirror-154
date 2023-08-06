#  Copyright 2021 Collate
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import textwrap

TABLE_ELASTICSEARCH_INDEX_MAPPING = textwrap.dedent(
    """
     {
    "mappings":{
          "properties": {
            "name": {
              "type":"text"
            },
            "display_name": {
              "type": "text"
            },
            "owner": {
              "properties": {
                "id": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 36
                    }
                  }
                },
                "type": {
                  "type": "text"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                        "ignore_above": 256
                    }
                 }
               },
              "fullyQualifiedName": {
                "type": "text"
              },
              "description": {
                "type": "text"
              },
              "deleted": {
               "type": "boolean"
              },
              "href": {
               "type": "text"
              }
             }
            },
            "deleted": {
              "type": "boolean"
            },
            "followers": {
              "type": "keyword"
            },
            "fqdn": {
              "type": "keyword"
            },
            "last_updated_timestamp": {
              "type": "date",
              "format": "epoch_second"
            },
            "description": {
              "type": "text"
            },
            "tier": {
              "type": "keyword"
            },
            "column_names": {
              "type":"text"
            },
            "column_descriptions": {
              "type": "text"
            },
            "tags": {
              "type": "keyword"
            },
            "service": {
             "properties": {
                "id": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 36
                    }
                  }
                },
                "type": {
                  "type": "text"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                        "ignore_above": 256
                    }
                 }
               },
              "fullyQualifiedName": {
                "type": "text"
              },
              "description": {
                "type": "text"
              },
              "deleted": {
               "type": "boolean"
              },
              "href": {
               "type": "text"
              }
             }
            },
            "service_type": {
              "type": "keyword"
            },
            "entity_type": {
              "type": "keyword"
            },
            "database": {
              "type": "keyword"
            },
            "database_schema": {
              "type": "keyword"
            },
            "suggest": {
              "type": "completion"
            },
            "column_suggest": {
              "type": "completion"
            },
            "schema_suggest": {
              "type": "completion"
            },
            "database_suggest": {
              "type": "completion"
            },
            "service_suggest": {
              "type": "completion"
            },
            "monthly_stats":{
              "type": "long"
            },
            "monthly_percentile_rank":{
              "type": "long"
            },
            "weekly_stats":{
              "type": "long"
            },
            "weekly_percentile_rank":{
              "type": "long"
            },
            "daily_percentile_rank": {
             "type": "long"
            },
            "daily_stats": {
              "type": "long"
            }
         }
      }
   }
    """
)

TOPIC_ELASTICSEARCH_INDEX_MAPPING = textwrap.dedent(
    """
    {
    "mappings":{
          "properties": {
            "name": {
              "type":"text"
            },
            "display_name": {
              "type": "text"
            },
            "owner": {
              "properties": {
                "id": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 36
                    }
                  }
                },
                "type": {
                  "type": "text"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                        "ignore_above": 256
                    }
                 }
               },
              "fullyQualifiedName": {
                "type": "text"
              },
              "description": {
                "type": "text"
              },
              "deleted": {
               "type": "boolean"
              },
              "href": {
               "type": "text"
              }
             }
            },
            "deleted": {
              "type": "boolean"
            },
            "followers": {
              "type": "keyword"
            },
            "fqdn": {
              "type": "keyword"
            },
            "last_updated_timestamp": {
              "type": "date",
              "format": "epoch_second"
            },
            "description": {
              "type": "text"
            },
            "tier": {
              "type": "keyword"
            },
            "tags": {
              "type": "keyword"
            },
            "service": {
              "properties": {
                "id": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 36
                    }
                  }
                },
                "type": {
                  "type": "text"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                        "ignore_above": 256
                    }
                 }
               },
              "fullyQualifiedName": {
                "type": "text"
              },
              "description": {
                "type": "text"
              },
              "deleted": {
               "type": "boolean"
              },
              "href": {
               "type": "text"
              }
             }
            },
            "service_type": {
              "type": "keyword"
            },
            "entity_type": {
              "type": "keyword"
            },
            "suggest": {
              "type": "completion"
            },
            "service_suggest": {
              "type": "completion"
            }
         }
      }
    }
    """
)

DASHBOARD_ELASTICSEARCH_INDEX_MAPPING = textwrap.dedent(
    """
    {
    "mappings":{
          "properties": {
            "name": {
              "type":"text"
            },
            "display_name": {
              "type": "text"
            }, 
            "owner": {
              "properties": {
                "id": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 36
                    }
                  }
                },
                "type": {
                  "type": "text"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                        "ignore_above": 256
                    }
                 }
               },
              "fullyQualifiedName": {
                "type": "text"
              },
              "description": {
                "type": "text"
              },
              "deleted": {
               "type": "boolean"
              },
              "href": {
               "type": "text"
              }
             }
            },
            "deleted": {
              "type": "boolean"
            },
            "fqdn": {
              "type": "keyword"
            },
            "followers": {
              "type": "keyword"
            },
            "last_updated_timestamp": {
              "type": "date",
              "format": "epoch_second"
            },
            "description": {
              "type": "text"
            },
            "chart_names": {
              "type":"text"
            },
            "chart_descriptions": {
              "type": "text"
            },
            "tier": {
              "type": "keyword"
            },
            "tags": {
              "type": "keyword"
            },
            "service": {
              "properties": {
                "id": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 36
                    }
                  }
                },
                "type": {
                  "type": "text"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                        "ignore_above": 256
                    }
                 }
               },
              "fullyQualifiedName": {
                "type": "text"
              },
              "description": {
                "type": "text"
              },
              "deleted": {
               "type": "boolean"
              },
              "href": {
               "type": "text"
              }
             }
            },
            "service_type": {
              "type": "keyword"
            },
            "entity_type": {
              "type": "keyword"
            },
            "suggest": {
              "type": "completion"
            },
            "chart_suggest": {
              "type": "completion"
            },
           "service_suggest": {
              "type": "completion"
            },
             "monthly_stats":{
              "type": "long"
            },
            "monthly_percentile_rank":{
              "type": "long"
            },
            "weekly_stats":{
              "type": "long"
            },
            "weekly_percentile_rank":{
              "type": "long"
            },
            "daily_percentile_rank": {
             "type": "long"
            },
            "daily_stats": {
              "type": "long"
            }
         }
      }
    }
    """
)

PIPELINE_ELASTICSEARCH_INDEX_MAPPING = textwrap.dedent(
    """
    {
    "mappings":{
          "properties": {
            "name": {
              "type":"text"
            },
            "display_name": {
              "type": "text"
            },
            "fqdn": {
              "type": "keyword"
            },
            "owner": {
              "properties": {
                "id": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 36
                    }
                  }
                },
                "type": {
                  "type": "text"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                        "ignore_above": 256
                    }
                 }
               },
              "fullyQualifiedName": {
                "type": "text"
              },
              "description": {
                "type": "text"
              },
              "deleted": {
               "type": "boolean"
              },
              "href": {
               "type": "text"
              }
             }
            },
            "deleted": {
              "type": "boolean"
            },
            "followers": {
              "type": "keyword"
            },
            "last_updated_timestamp": {
              "type": "date",
              "format": "epoch_second"
            },
            "description": {
              "type": "text"
            },
            "task_names": {
              "type":"text"
            },
            "task_descriptions": {
              "type": "text"
            },
            "tier": {
              "type": "keyword"
            },
            "tags": {
              "type": "keyword"
            },
            "service": {
              "properties": {
                "id": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 36
                    }
                  }
                },
                "type": {
                  "type": "text"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                        "ignore_above": 256
                    }
                 }
               },
              "fullyQualifiedName": {
                "type": "text"
              },
              "description": {
                "type": "text"
              },
              "deleted": {
               "type": "boolean"
              },
              "href": {
               "type": "text"
              }
             }
            },
            "service_type": {
              "type": "keyword"
            },
            "entity_type": {
              "type": "keyword"
            },
            "suggest": {
              "type": "completion"
            },
            "task_suggest": {
              "type": "completion"
            },
           "service_suggest": {
             "type": "completion"
           }
         }
      }
    }
    """
)

USER_ELASTICSEARCH_INDEX_MAPPING = textwrap.dedent(
    """
      {
 	"mappings": {
 		"properties": {
 			"name": {
 				"type": "text"
 			},
 			"display_name": {
 				"type": "text"
 			},
 			"email": {
 				"type": "text"
 			},
 			"last_updated_timestamp": {
 				"type": "date",
 				"format": "epoch_second"
 			},
 			"entity_type": {
 				"type": "keyword"
 			},
 			"teams": {
 				"properties": {
		"id": {
			"type": "keyword",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 36
				}
			}
		},
		"type": {
			"type": "text"
		},
		"name": {
			"type": "keyword",
			"fields": {
				"keyword": {
					"type": "keyword",
					"ignore_above": 256
				}
			}
		},
		"fullyQualifiedName": {
			"type": "text"
		},
		"description": {
			"type": "text"
		},
		"deleted": {
			"type": "boolean"
		},
		"href": {
			"type": "text"
		}
	}
 			},

 			"deleted": {
 				"type": "boolean"
 			},
 			"suggest": {
 				"type": "completion"
 			},
 			"roles": {
 				"properties": {
 					"id": {
 						"type": "keyword",
 						"fields": {
 							"keyword": {
 								"type": "keyword",
 								"ignore_above": 36
 							}
 						}
 					},
 					"type": {
 						"type": "text"
 					},
 					"name": {
 						"type": "keyword",
 						"fields": {
 							"keyword": {
 								"type": "keyword",
 								"ignore_above": 256
 							}
 						}
 					},
 					"fullyQualifiedName": {
 						"type": "text"
 					},
 					"description": {
 						"type": "text"
 					},
 					"deleted": {
 						"type": "boolean"
 					},
 					"href": {
 						"type": "text"
 					}
 				}
 			}
 		}
 	}
 }
    """
)

TEAM_ELASTICSEARCH_INDEX_MAPPING = textwrap.dedent(
    """
     {
 	"mappings": {
 		"properties": {
 			"name": {
 				"type": "text"
 			},
 			"display_name": {
 				"type": "text"
 			},
 			"last_updated_timestamp": {
 				"type": "date",
 				"format": "epoch_second"
 			},
 			"entity_type": {
 				"type": "keyword"
 			},
 			"deleted": {
 				"type": "boolean"
 			},
 			"users": {
 				"properties": {
 					"id": {
 						"type": "keyword",
 						"fields": {
 							"keyword": {
 								"type": "keyword",
 								"ignore_above": 36
 							}
 						}
 					},
 					"type": {
 						"type": "text"
 					},
 					"name": {
 						"type": "keyword",
 						"fields": {
 							"keyword": {
 								"type": "keyword",
 								"ignore_above": 256
 							}
 						}
 					},
 					"fullyQualifiedName": {
 						"type": "text"
 					},
 					"description": {
 						"type": "text"
 					},
 					"deleted": {
 						"type": "boolean"
 					},
 					"href": {
 						"type": "text"
 					}
 				}
 			},
 			"owns": {
 				"type": "keyword"
 			},
 			"default_roles": {
 				"properties": {
 					"id": {
 						"type": "keyword",
 						"fields": {
 							"keyword": {
 								"type": "keyword",
 								"ignore_above": 36
 							}
 						}
 					},
 					"type": {
 						"type": "text"
 					},
 					"name": {
 						"type": "keyword",
 						"fields": {
 							"keyword": {
 								"type": "keyword",
 								"ignore_above": 256
 							}
 						}
 					},
 					"fullyQualifiedName": {
 						"type": "text"
 					},
 					"description": {
 						"type": "text"
 					},
 					"deleted": {
 						"type": "boolean"
 					},
 					"href": {
 						"type": "text"
 					}
 				}
 			},
 			"suggest": {
 				"type": "completion"
 			}
 		}
 	}
 }
    """
)

GLOSSARY_TERM_ELASTICSEARCH_INDEX_MAPPING = textwrap.dedent(
    """
     {
    "mappings": {
        "properties": {
          "name": {
            "type": "text"
          },
          "display_name": {
            "type": "text"
          },
           "fqdn": {
              "type": "keyword"
            },
          "owner": {
              "properties": {
                "id": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 36
                    }
                  }
                },
                "type": {
                  "type": "text"
                },
                "name": {
                  "type": "keyword",
                  "fields": {
                    "keyword": {
                      "type": "keyword",
                        "ignore_above": 256
                    }
                 }
               },
              "fullyQualifiedName": {
                "type": "text"
              },
              "description": {
                "type": "text"
              },
              "deleted": {
               "type": "boolean"
              },
              "href": {
               "type": "text"
              }
             }
            },
         "last_updated_timestamp": {
            "type": "date",
            "format": "epoch_second"
         },
         "description": {
            "type": "text"
         },
        "glossary_name": {
            "type": "keyword"
         },
        "glossary_id": {
            "type": "keyword"
        },
        "deleted": {
            "type": "boolean"
        },
        "status": {
            "type": "keyword"
        },
        "tags": {
            "type": "keyword"
        },
        "entity_type": {
            "type": "keyword"
        },
        "suggest": {
            "type": "completion"
        }
      }
    }
  }
    """
)

MLMODEL_ELASTICSEARCH_INDEX_MAPPING = textwrap.dedent(
    """
     {
  	"mappings": {
  		"properties": {
  			"name": {
  				"type": "text"
  			},
  			"display_name": {
  				"type": "text"
  			},
  			"fqdn": {
  				"type": "keyword"
  			},
  			"algorithm": {
  				"type": "keyword"
  			},
  			"ml_features": {
  				"type": "keyword"
  			},
  			"ml_hyper_parameters": {
  				"type": "keyword"
  			},
  			"deleted": {
  				"type": "boolean"
  			},
  			"owner": {
  				"properties": {
  					"id": {
  						"type": "keyword",
  						"fields": {
  							"keyword": {
  								"type": "keyword",
  								"ignore_above": 128
  							}
  						}
  					},
  					"type": {
  						"type": "text"
  					},
  					"name": {
  						"type": "keyword",
  						"fields": {
  							"keyword": {
  								"type": "keyword",
  								"ignore_above": 256
  							}
  						}
  					},
  					"fullyQualifiedName": {
  						"type": "text"
  					},
  					"description": {
  						"type": "text"
  					},
  					"deleted": {
  						"type": "boolean"
  					},
  					"href": {
  						"type": "text"
  					}
  				}
  			},
  			"followers": {
  				"type": "keyword"
  			},
  			"last_updated_timestamp": {
  				"type": "date",
  				"format": "epoch_second"
  			},
  			"description": {
  				"type": "text"
  			},
  			"tier": {
  				"type": "keyword"
  			},
  			"tags": {
  				"type": "keyword"
  			},
  			"entity_type": {
  				"type": "keyword"
  			},
  			"suggest": {
  				"type": "completion"
  			},
  			"service_suggest": {
               "type": "completion"
            },
  			"monthly_stats": {
  				"type": "long"
  			},
  			"monthly_percentile_rank": {
  				"type": "long"
  			},
  			"weekly_stats": {
  				"type": "long"
  			},
  			"weekly_percentile_rank": {
  				"type": "long"
  			},
  			"daily_percentile_rank": {
  				"type": "long"
  			},
  			"daily_stats": {
  				"type": "long"
  			}
  		}
  	}

  }
    """
)
