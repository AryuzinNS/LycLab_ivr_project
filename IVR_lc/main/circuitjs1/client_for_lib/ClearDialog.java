/*    
    Copyright (C) Paul Falstad and Iain Sharp
    
    This file is part of CircuitJS1.

    CircuitJS1 is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    CircuitJS1 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with CircuitJS1.  If not, see <http://www.gnu.org/licenses/>.
*/

package com.lushprojects.circuitjs1.client;


import com.google.gwt.user.client.ui.DialogBox;
import com.google.gwt.user.client.ui.HorizontalPanel;
import com.google.gwt.user.client.ui.Button;
import com.google.gwt.user.client.ui.VerticalPanel;
import com.google.gwt.event.dom.client.ClickHandler;
import com.google.gwt.event.dom.client.ClickEvent;
import com.google.gwt.user.client.ui.Label;
    public class ClearDialog extends DialogBox {
    	
    		VerticalPanel vp;
    		HorizontalPanel hp;
    		CirSim sim;
    		Label l;
    		public ClearDialog(CirSim asim) {
    		    super();
    		    sim= asim;
    		    Button okButton,undoButton;
    		    vp=new VerticalPanel();
    		    vp.setStylePrimaryName("scrollbars");
    		    setWidget(vp);
    		    setText(CirSim.LS("Confirm Operation"));
    		    l = new Label(CirSim.LS("Do you want to clear the page?"));
    		    l.setStylePrimaryName("labelForSlider");
    		    vp.add(l);
    		    hp = new HorizontalPanel();
    		    vp.add(hp);
    		    okButton = new Button(CirSim.LS("OK"));
    		    okButton.setStyleName("topButton");
    		    hp.add(okButton);
    		    okButton.addClickHandler(new ClickHandler() {
    				public void onClick(ClickEvent event) {
    				    sim.pushUndo();
    				    sim.readSetupFile("blank.txt", "Blank Circuit");
    				    closeDialog();
    				}
    		    });
    		    undoButton = new Button(CirSim.LS("Cancel"));
    		    undoButton.setStyleName("topButton");
    		    hp.add(undoButton);
    		    undoButton.addClickHandler(new ClickHandler() {
    				public void onClick(ClickEvent event) {
    				    closeDialog();
    				}
    		    });
    		    this.center();
    		}
    	
    		protected void closeDialog()
    		{
    		    this.hide();
    		}
    
    }