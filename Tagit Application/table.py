# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 16:19:42 2018

@author: Graccolab
"""

       <table>
           <tr>
               <th>name_of_list</th>
               <th>values</th>
           </tr>

           {% for key, values in better_choices.items() %}
           <tr>
               <td>{{key}}</td>
               <td>
               <table>
                  <tr>
                    <th>number of follower</th>
                  </tr>
                  <tr>
                      <td>{{values}}</td>
                  {% endfor %}
                  </tr>
               </td>
            </tr>
           {% endfor %}

       </table>