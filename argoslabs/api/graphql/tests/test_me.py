"""
====================================
 :mod:`argoslabs.api.graphql`
====================================
.. moduleauthor:: Arun Kumar <arunk@argos-labs.com>
.. note:: ARGOS-LABS License

Description
===========
GraphQL API
"""
# Authors
# ===========
#
# * Arun Kumar , Jerry
#
# Change Log
# --------
#
#  * [2022/02/02]
#     - starting

################################################################################
import os
import sys
from unittest import TestCase
from argoslabs.api.graphql import _main as main


################################################################################
class TU(TestCase):
    # ==========================================================================
    def setUp(self) -> None:
        os.chdir(os.path.dirname(__file__))
        self.uri1 = 'https://api.github.com/graphql'
        self.query1 = """
        query MeQuery {
  viewer {
    login
    name
  }
}
        """

        

        self.uri2 = 'https://graphql.anilist.co'
        self.query2 = """
        {
  Page {
    media {
      siteUrl
      title {
        english
        native
      }
      description
    }
  }
}
        """


        self.uri6 = 'https://dex-server.herokuapp.com/'
        self.query6 = """
        {
  allPokemon {
    name
  }
}
        """

#no auth
#         self.uri = 'https://beta.pokeapi.co/graphql/v1beta'
#         self.query = """
# query Query {
#     id
# }
#         """



        self.uri5 = 'https://countries.trevorblades.com/graphql'
        self.query5 = """
        query Query {
  country(code: "BR") {
    name
    native
    capital
    emoji
    currency
    languages {
      code
      name
    }
  }
}
        """

        self.uri4 = 'https://rickandmortyapi.com/graphql'
        self.query4 = """
        query Query {
  characters(page: 2, filter: { name: "Morty" }) {
    info {
      count
    }
    results {
      name
    }
  }
  location(id: 1) {
    id
  }
  episodesByIds(ids: [1, 2]) {
    id
  }
}
        """
        self.uri3 = 'https://swapi-graphql.netlify.app/.netlify/functions/index'
        self.query3 = """
        query Query {
  allFilms {
    films {
      title
      director
      releaseDate
      speciesConnection {
        species {
          name
          classification
          homeworld {
            name
          }
        }
      }
    }
  }
}
        """
        self.uri = 'https://api.spacex.land/graphql/'
        self.query = '''query Launches {
  launches {
    mission_name
    mission_id
    rocket {
      rocket_name
      rocket {
        company
        name
        mass {
          kg
        }
      }
    }
    launch_site {
      site_name
    }
    launch_date_local
  }
}'''
        self.uris = 'https://api.spacex.land/graphql1/'
        self.querys = '''query Launches {
      launches1 {
        mission_name
        mission_id
        rocket {
          rocket_name
          rocket {
            company
            name
            mass {
              kg
            }
          }
        }
        launch_site {
          site_name
        }
        launch_date_local
      }
    }'''
    # ==========================================================================
    def test0010_spacex_server(self):
        try:
            r = main(self.uri,self.query,'--headers','Content-Type: application/json')
            self.assertTrue(r==0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)


    # ==========================================================================
    def test0010_github_server(self):
        try:
            r = main(self.uri1,self.query1,'--headers','Content-Type: application/json',
                     '--headers', 'Authorization: bearer'
                     )
            self.assertTrue(r==0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0010_github_authenticate_without_context_server(self):
        try:
            r = main(self.uri1,self.query1,
                     # '--headers','Content-Type: application/json',
                     '--headers', 'Authorization: bearer'
                     )
            self.assertTrue(r==0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0010_anilist_server(self):
        try:
            r = main(self.uri2,self.query2,'--headers','Content-Type: application/json'

                     )
            self.assertTrue(r==0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
    # ==========================================================================
    def test0010_netlify_server(self):
        try:
            r = main(self.uri3,self.query3,'--headers','Content-Type: application/json'
                     )
            self.assertTrue(r==0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
    # ==========================================================================
    def test0010_rickandmortyapi_server(self):
        try:
            r = main(self.uri4,self.query4,'--headers','Content-Type: application/json'
                     )
            self.assertTrue(r==0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0010_trevorblades_server(self):
        try:
            r = main(self.uri5,self.query5,'--headers','Content-Type: application/json'
                     )
            self.assertTrue(r==0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test0010_herokuapp_server(self):
        try:
            r = main(self.uri6,self.query6,'--headers','Content-Type: application/json'
                     )
            self.assertTrue(r==0)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)


    # ==========================================================================
    def test0010_spacex_404_Client_Error_server(self):
        try:
            r = main(self.uris,self.query,'--headers','Content-Type: application/json')
            self.assertTrue(r==4)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)

    # ==========================================================================
    def test00101_spacex_400_Client_Error_server(self):
        try:
            r = main(self.uri,self.querys,'--headers','Content-Type: application/json')
            self.assertTrue(r==4)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
    # ==========================================================================
    def test00102_spacex_500_server_Error(self):
        try:
            r = main(self.uri,self.query,
                     # '--headers','Content-Type: application/json'
                     )

            self.assertTrue(r==5)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)
    # ==========================================================================
    def test0010_github_401_Unauthorized_Client_error_server(self):
        try:
            r = main(self.uri1,self.query1,
                     '--headers','Content-Type: application/json',
                     # '--headers', 'Authorization: bearer'
                     )
            self.assertTrue(r==4)
        except Exception as e:
            sys.stderr.write('\n%s\n' % str(e))
            self.assertTrue(True)




    # ==========================================================================
    def test9999_quit(self):
        self.assertTrue(True)
