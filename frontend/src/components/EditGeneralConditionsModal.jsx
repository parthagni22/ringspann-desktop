import React, { useState, useEffect } from 'react';

const DEFAULT_CONDITIONS = [
  {
    title: "1. Scope of application",
    content: "These Terms apply to the sale and supply of power transmission parts (\"Products\") as per purchase orders issued by the Customer and accepted by the Company. Where applicable, the Company may manufacture or modify Products based on the Customer's specific requirements, subject to a written agreement on design specifications, delivery timelines, and pricing. The following Terms shall apply to all deliveries of our products, except as modified by express agreement accepted in writing by both parties. These Terms do not cover installation, commissioning, or maintenance services, if provided by the Company."
  },
  {
    title: "2. Definitions",
    content: "a. Confidential Information shall mean any and all materials and information concerning the Company, including without limitation its directors, officers, employees, subsidiaries and/or group companies, vendors, users and customers or any third party with which the Company associates (collectively, \"Affiliates\"), disclosed by the Company whether or not such information is expressly marked or designated as confidential information, including, without limitation, computer programs, software (including source code, object code and machine code) relating to the foregoing, technical drawings, algorithms, pricing information.\n\nb. Intellectual Property Rights (IPR) shall mean all drawings, designs, models, specifications, documentation, software, inventions, techniques, processes, business methods, know-how, mask-works, copyrights, copyrightable materials, patents, trademarks, trade secrets, and any other information or materials protected under any intellectual property laws in effect anywhere in the world, and any applications, registrations or filings relating thereto."
  },
  {
    title: "3. Governing Terms",
    content: "a. The following documents govern the transaction - Any Company-issued quotation, order acknowledgment, invoice, or written agreement.\n\nb. To the extent possible, the terms contained in these documents shall be read harmoniously. However, in the event of any conflict between these Terms and another document, these Terms shall prevail. These Terms shall prevail over any contrary terms proposed by the Customer. No additional terms shall be deemed part of these Terms unless expressly agreed to in writing and signed by an authorized representative of the Company. For the avoidance of doubt, the following shall not form part of these Terms:\n(i) Any terms referenced by the Customer in its purchase orders or other documents, except for product description, quantity, and pricing that align with the Company's quotation, acknowledgment, invoice, or a separate signed agreement;\n(ii) Customer's standard terms and conditions of purchase, quality policy, supplier guidelines, or similar operational policies;\n(iii) Any terms on the Customer's website or electronic procurement portal, even if the Company is required to click \"accept,\" \"agree,\" or similar prompts in order to access or submit order-related information."
  },
  {
    title: "4. Terms of Payment and Pricing",
    content: "a. Unless otherwise agreed, Customer shall make payment of 100% of the invoiced amount in advance against a Proforma Invoice issued by the Company. In the event of any delay in payment beyond the agreed timeline, the Company reserves the right to charge interest on the overdue amount at a rate of 8% above the prevailing discount rate of the Reserve Bank of India.\n\nb. The Customer shall not withhold payment or make any deductions from the invoiced amount on account of complaints regarding the Products, unless such liability is acknowledged in writing by the Company. Goods and Services Tax (GST) and any other applicable taxes or duties shall be levied in accordance with the relevant HSN Code and prevailing laws at the time of invoicing.\n\nc. Unless otherwise agreed in writing, the Company reserves the right to revise prices or apply a surcharge at any time to reflect changes in input costs, including but not limited to raw material prices, labor costs.\n\nd. In cases where specialized tools, gauges, or clamping devices are required to execute a custom order, such items shall be invoiced separately to the Customer. However, ownership of these tools and devices shall remain exclusively with the Company upon completion of the order. Ownership of the Products shall remain with the Company until full payment of the purchase price has been received.\n\ne. A Packing and Forwarding (P&F) charge of 2% shall be applicable on the price per Purchase Order. In cases where no P&F charge is applicable, the Company shall utilize its standard packing method for dispatch. Any special packaging requirements requested by the Customer may attract additional charges, which will be communicated separately."
  },
  {
    title: "5. Orders and Acceptance",
    content: "a. All orders must be submitted in writing and clearly specify the type and quantity of Products, delivery address, required delivery date, and any applicable reference to quotations or prior correspondence.\n\nb. Orders become binding only upon written acceptance by the Company. All dimensions, weights, illustrations, and technical drawings provided prior to order confirmation are indicative only and not contractually binding, unless confirmed in writing. The scope, specifications, and type of Products to be delivered shall be determined solely by the Company's written order confirmation.\n\nc. Any modifications requested by the Customer after order confirmation must be approved in writing by the Company and may be subject to revised terms, including pricing and delivery schedule. The Customer may not cancel or amend an order after confirmation without the prior written consent of the Company. Any such change may be subject to charges as reasonably determined by the Company."
  },
  {
    title: "6. Delivery",
    content: "a. All prices are quoted on an EX Works Chakan basis (Incoterms 2020), unless otherwise agreed.\n\nb. The delivery period shall commence only after all technical specifications and contractual details have been mutually agreed upon in writing by both Parties"
  },
  {
    title: "7. Force Majeure",
    content: "a. The Company shall not be liable for any delay in delivery or failure to fulfill an order caused by circumstances beyond its reasonable control, including but not limited to acts of God, natural disasters, pandemics, labor unrest, strikes, lockouts, supply chain disruptions, power or equipment failure, operating difficulties, delays by subcontractors or suppliers, transportation issues, port congestion, embargoes, or any governmental or regulatory actions (\"Force Majeure Event(s)\"). In the event of any such Force Majeure Event(s), the Company shall be entitled to an appropriate extension of the delivery period. The Company will notify the Customer of the occurrence and expected duration of such delay as soon as reasonably practicable. Any claims for penalties, liquidated damages, or other compensation due to delayed delivery shall be excluded unless specifically agreed upon in writing at the time of placing the order. The Customer shall not be entitled to cancel the order, reject, or refuse to accept delivery of the Products due to delays arising from Force Majeure Events or other reasons unless the Products, upon delivery, are found not to conform to the warranty obligations set forth in this Agreement."
  },
  {
    title: "8. Representations and Warranty",
    content: "a. The Customer shall inspect the Products immediately upon receipt. Any claims for defects or non-conformities must be reported to the Company in writing within seven (7) days of receipt of the shipment. Failure to notify the Company within this period shall constitute acceptance of the Products as delivered and a waiver of any such claims.\n\nb. Unless otherwise expressly agreed in writing, each Product shall be covered under the limited warranty by the Company that every Product has been manufactured in accordance with applicable law and that it meets its specifications, it will be free from defects in materials or workmanship, provided it is stored, used and handled under the conditions recommended by Company. The Company warranty is for a period of twelve (12) months from the date of commissioning or eighteen (18) months from the date of dispatch, whichever occurs earlier. In the event of a valid deficiency claim, the Company's sole obligation shall be, at its discretion, to either:\n(i) Repair the defective component(s), or\n(ii) Replace the defective component(s), free of charge, provided that such components are returned to the Company's premises in the original or equivalent protective packaging.\n\nc. The Company shall be liable only for:\n(i) Defects arising from its own design or manufacturing faults; and\n(ii) Material defects that the Company should have reasonably discovered through due diligence.\n\nd. The Company shall not be liable for any claims, losses, or damages arising out of or relating to the following circumstances, whether direct or indirect:\n(i) Normal wear and tear of the Products under regular operating conditions, including deterioration due to environmental exposure, usage, or time;\n(ii) Improper handling, incorrect storage, misuse, negligence, or operation of the Products in a manner inconsistent with the Product specifications, manuals, or any written instructions provided by the Company;\n(iii) Any modification of the Products undertaken by the Customer or any third party;\n(iv) Use of non-original replacement parts, components, or consumables with the Products;\n(v) Any force majeure events including but not limited to fire, flood, act of God, civil unrest, strikes, war, pandemic, or government-imposed restrictions;\n(vi) Consequential or indirect damages including, but not limited to, loss of production, business interruption, penalties for delay, freight costs, costs of disassembly/reassembly, or damage to other machinery or equipment.\n(vii) Any claims arising after the expiration of the applicable warranty period.\n\ne. All other terms and conditions shall be as specified in the Installation and Operating Manual issued by the Company.\n\nf. The Customer represents that it has all the requisite power to execute these Terms and to perform its obligations hereunder, and the person(s) implementing these Terms on its behalf are duly authorised. These Terms are legally binding upon it and it does not conflict with any agreement, instrument or understanding, oral or written, to which it is a party or by which it may be bound."
  },
  {
    title: "9. Indemnity and Limitation of Liability",
    content: "a. The Customer shall indemnify and hold harmless the Company and its affiliates (\"Indemnified Parties\") from any claims, losses, liabilities, damages, or expenses (including legal fees) arising from:\n(i) any breach of these Terms;\n(ii) any negligence, willful misconduct, or legal violation by the Customer or its representatives;\n(iii) any misuse, unauthorized modification, or improper handling of the Products by the Customer or parties under its control;\n(iv) any claim that Customer-provided specifications, drawings, or instructions infringe third-party intellectual property rights.\n\nb. The Company shall not be liable for any indirect, incidental, consequential, punitive, or special damages, including loss of profits, data, or business, even if advised of such possibility. These limitations and exclusions apply regardless of the form or basis of the claim."
  },
  {
    title: "10. Term and Termination",
    content: "These Terms shall remain in effect until completion of the obligations by both Parties and may be terminated earlier by mutual written consent or for material breach not remedied within a reasonable period as discussed in writing by the Customer and the Company."
  },
  {
    title: "11. Confidentiality Obligations",
    content: "The Customer agrees to keep confidential all technical, commercial, and business information received from the Company. The Customer must protect the confidentiality of any information shared by the Company for a period of two (2) years after termination. Breach may result in a fixed penalty (amount to be agreed) per violation, in addition to potential damage claims. The Company also retains the right to claim indemnification of damage caused to it by the disclosure of the information."
  },
  {
    title: "12. Governing Law and Jurisdiction",
    content: "These Terms are governed by the laws of India. Disputes shall be subject to the exclusive jurisdiction of courts in Pune, Maharashtra, India."
  }
];

const EditGeneralConditionsModal = ({ isOpen, onClose, onSave, currentConditions }) => {
  const [conditions, setConditions] = useState(DEFAULT_CONDITIONS);

  useEffect(() => {
    if (currentConditions) {
      parseConditions(currentConditions);
    }
  }, [currentConditions]);

  const parseConditions = (conditionsText) => {
    if (!conditionsText) return;
    
    const parsed = [];
    const lines = conditionsText.split('\n');
    let currentCondition = null;
    
    lines.forEach(line => {
      const titleMatch = line.match(/^(\d+\.\s+.+?):/);
      if (titleMatch) {
        if (currentCondition) {
          parsed.push(currentCondition);
        }
        currentCondition = {
          title: titleMatch[1],
          content: line.substring(titleMatch[0].length).trim()
        };
      } else if (currentCondition && line.trim()) {
        currentCondition.content += ' ' + line.trim();
      }
    });
    
    if (currentCondition) {
      parsed.push(currentCondition);
    }
    
    if (parsed.length > 0) {
      setConditions(parsed);
    }
  };

  const handleConditionChange = (index, field, value) => {
    const newConditions = [...conditions];
    newConditions[index][field] = value;
    setConditions(newConditions);
  };

  const handleAddCondition = () => {
    setConditions([...conditions, {
      title: `${conditions.length + 1}. New Condition`,
      content: ''
    }]);
  };

  const handleRemoveCondition = (index) => {
    if (conditions.length === 1) {
      alert('At least one condition is required');
      return;
    }
    setConditions(conditions.filter((_, i) => i !== index));
  };

  const handleSave = async () => {
    const formattedConditions = conditions.map(c => 
      `${c.title}: ${c.content}`
    ).join('\n\n');
    
    await onSave(formattedConditions);
    onClose();
  };

  const handleResetDefaults = () => {
    setConditions(DEFAULT_CONDITIONS);
  };

  if (!isOpen) return null;

  return (
    <div style={styles.overlay}>
      <div style={styles.modal}>
        <div style={styles.header}>
          <h2 style={styles.title}>Edit General Conditions</h2>
          <button onClick={onClose} style={styles.closeBtn}>×</button>
        </div>

        <div style={styles.content}>
          {conditions.map((condition, index) => (
            <div key={index} style={styles.conditionBlock}>
              <div style={styles.conditionHeader}>
                <input
                  type="text"
                  value={condition.title}
                  onChange={(e) => handleConditionChange(index, 'title', e.target.value)}
                  style={styles.titleInput}
                />
                {conditions.length > 1 && (
                  <button
                    onClick={() => handleRemoveCondition(index)}
                    style={styles.removeBtn}
                  >
                    Remove
                  </button>
                )}
              </div>
              <textarea
                value={condition.content}
                onChange={(e) => handleConditionChange(index, 'content', e.target.value)}
                style={styles.textarea}
                rows="8"
                placeholder="Enter condition details..."
              />
            </div>
          ))}

          <button onClick={handleAddCondition} style={styles.addBtn}>
            + Add New Condition
          </button>
        </div>

        <div style={styles.footer}>
          <button onClick={handleResetDefaults} style={styles.resetBtn}>
            Reset to Defaults
          </button>
          <div style={styles.actionBtns}>
            <button onClick={handleSave} style={styles.saveBtn}>Save</button>
            <button onClick={onClose} style={styles.cancelBtn}>Cancel</button>
          </div>
        </div>
      </div>
    </div>
  );
};

const styles = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.5)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000
  },
  modal: {
    backgroundColor: 'white',
    borderRadius: '8px',
    width: '900px',
    maxHeight: '90vh',
    display: 'flex',
    flexDirection: 'column',
    boxShadow: '0 4px 20px rgba(0,0,0,0.3)'
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '20px',
    borderBottom: '1px solid #ddd',
    backgroundColor: '#ff6600'
  },
  title: {
    margin: 0,
    color: 'white',
    fontSize: '20px'
  },
  closeBtn: {
    background: 'none',
    border: 'none',
    fontSize: '28px',
    color: 'white',
    cursor: 'pointer',
    padding: '0',
    width: '30px',
    height: '30px'
  },
  content: {
    padding: '20px',
    overflowY: 'auto',
    flex: 1
  },
  conditionBlock: {
    marginBottom: '25px',
    padding: '20px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    backgroundColor: '#f9f9f9'
  },
  conditionHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px'
  },
  titleInput: {
    flex: 1,
    padding: '10px',
    fontSize: '15px',
    fontWeight: 'bold',
    border: '1px solid #ccc',
    borderRadius: '4px',
    marginRight: '10px'
  },
  textarea: {
    width: '100%',
    padding: '12px',
    fontSize: '14px',
    border: '1px solid #ccc',
    borderRadius: '4px',
    fontFamily: 'Arial, sans-serif',
    resize: 'vertical',
    lineHeight: '1.5'
  },
  removeBtn: {
    padding: '8px 15px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px'
  },
  addBtn: {
    padding: '12px 24px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '15px',
    fontWeight: '600',
    marginTop: '10px'
  },
  footer: {
    padding: '15px 20px',
    borderTop: '1px solid #ddd',
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
  },
  resetBtn: {
    padding: '10px 20px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer'
  },
  actionBtns: {
    display: 'flex',
    gap: '10px'
  },
  saveBtn: {
    padding: '10px 30px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '15px'
  },
  cancelBtn: {
    padding: '10px 30px',
    backgroundColor: '#6c757d',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '15px'
  }
};

export default EditGeneralConditionsModal;
































// import React, { useState, useEffect } from 'react';

// const DEFAULT_CONDITIONS = [
//   {
//     title: "1. Scope of application",
//     content: "These Terms apply to the sale and supply of power transmission parts (\"Products\") as per purchase orders issued by the Customer and accepted by the Company. Where applicable, the Company may manufacture or modify Products based on the Customer's specific requirements, subject to a written agreement on design specifications, delivery timelines, and pricing. The following Terms shall apply to all deliveries of our products, except as modified by express agreement accepted in writing by both parties. These Terms do not cover installation, commissioning, or maintenance services, if provided by the Company."
//   },
//   {
//     title: "2. Definitions",
//     content: "a. Confidential Information shall mean any and all materials and information concerning the Company, including without limitation its directors, officers, employees, subsidiaries and/or group companies, vendors, users and customers or any third party with which the Company associates (collectively, \"Affiliates\"), disclosed by the Company whether or not such information is expressly marked or designated as confidential information, including, without limitation, computer programs, software (including source code, object code and machine code) relating to the foregoing, technical drawings, algorithms, pricing information.\n\nb. Intellectual Property Rights (IPR) shall mean all drawings, designs, models, specifications, documentation, software, inventions, techniques, processes, business methods, know-how, mask-works, copyrights, copyrightable materials, patents, trademarks, trade secrets, and any other information or materials protected under any intellectual property laws in effect anywhere in the world, and any applications, registrations or filings relating thereto."
//   },
//   {
//     title: "3. Governing Terms",
//     content: "a. The following documents govern the transaction - Any Company-issued quotation, order acknowledgment, invoice, or written agreement.\n\nb. To the extent possible, the terms contained in these documents shall be read harmoniously. However, in the event of any conflict between these Terms and another document, these Terms shall prevail. These Terms shall prevail over any contrary terms proposed by the Customer. No additional terms shall be deemed part of these Terms unless expressly agreed to in writing and signed by an authorized representative of the Company. For the avoidance of doubt, the following shall not form part of these Terms:\n(i) Any terms referenced by the Customer in its purchase orders or other documents, except for product description, quantity, and pricing that align with the Company's quotation, acknowledgment, invoice, or a separate signed agreement;\n(ii) Customer's standard terms and conditions of purchase, quality policy, supplier guidelines, or similar operational policies;\n(iii) Any terms on the Customer's website or electronic procurement portal, even if the Company is required to click \"accept,\" \"agree,\" or similar prompts in order to access or submit order-related information."
//   },
//   {
//     title: "4. Terms of Payment and Pricing",
//     content: "a. Unless otherwise agreed, Customer shall make payment of 100% of the invoiced amount in advance against a Proforma Invoice issued by the Company. In the event of any delay in payment beyond the agreed timeline, the Company reserves the right to charge interest on the overdue amount at a rate of 8% above the prevailing discount rate of the Reserve Bank of India.\n\nb. The Customer shall not withhold payment or make any deductions from the invoiced amount on account of complaints regarding the Products, unless such liability is acknowledged in writing by the Company. Goods and Services Tax (GST) and any other applicable taxes or duties shall be levied in accordance with the relevant HSN Code and prevailing laws at the time of invoicing.\n\nc. Unless otherwise agreed in writing, the Company reserves the right to revise prices or apply a surcharge at any time to reflect changes in input costs, including but not limited to raw material prices, labor costs.\n\nd. In cases where specialized tools, gauges, or clamping devices are required to execute a custom order, such items shall be invoiced separately to the Customer. However, ownership of these tools and devices shall remain exclusively with the Company upon completion of the order. Ownership of the Products shall remain with the Company until full payment of the purchase price has been received.\n\ne. A Packing and Forwarding (P&F) charge of 2% shall be applicable on the price per Purchase Order. In cases where no P&F charge is applicable, the Company shall utilize its standard packing method for dispatch. Any special packaging requirements requested by the Customer may attract additional charges, which will be communicated separately."
//   },
//   {
//     title: "5. Orders and Acceptance",
//     content: "a. All orders must be submitted in writing and clearly specify the type and quantity of Products, delivery address, required delivery date, and any applicable reference to quotations or prior correspondence.\n\nb. Orders become binding only upon written acceptance by the Company. All dimensions, weights, illustrations, and technical drawings provided prior to order confirmation are indicative only and not contractually binding, unless confirmed in writing. The scope, specifications, and type of Products to be delivered shall be determined solely by the Company's written order confirmation.\n\nc. Any modifications requested by the Customer after order confirmation must be approved in writing by the Company and may be subject to revised terms, including pricing and delivery schedule. The Customer may not cancel or amend an order after confirmation without the prior written consent of the Company. Any such change may be subject to charges as reasonably determined by the Company."
//   },
//   {
//     title: "6. Delivery",
//     content: "a. All prices are quoted on an EX Works Chakan basis (Incoterms 2020), unless otherwise agreed.\n\nb. The delivery period shall commence only after all technical specifications and contractual details have been mutually agreed upon in writing by both Parties"
//   },
//   {
//     title: "7. Force Majeure",
//     content: "a. The Company shall not be liable for any delay in delivery or failure to fulfill an order caused by circumstances beyond its reasonable control, including but not limited to acts of God, natural disasters, pandemics, labor unrest, strikes, lockouts, supply chain disruptions, power or equipment failure, operating difficulties, delays by subcontractors or suppliers, transportation issues, port congestion, embargoes, or any governmental or regulatory actions (\"Force Majeure Event(s)\"). In the event of any such Force Majeure Event(s), the Company shall be entitled to an appropriate extension of the delivery period. The Company will notify the Customer of the occurrence and expected duration of such delay as soon as reasonably practicable. Any claims for penalties, liquidated damages, or other compensation due to delayed delivery shall be excluded unless specifically agreed upon in writing at the time of placing the order. The Customer shall not be entitled to cancel the order, reject, or refuse to accept delivery of the Products due to delays arising from Force Majeure Events or other reasons unless the Products, upon delivery, are found not to conform to the warranty obligations set forth in this Agreement."
//   },
//   {
//     title: "8. Representations and Warranty",
//     content: "a. The Customer shall inspect the Products immediately upon receipt. Any claims for defects or non-conformities must be reported to the Company in writing within seven (7) days of receipt of the shipment. Failure to notify the Company within this period shall constitute acceptance of the Products as delivered and a waiver of any such claims.\n\nb. Unless otherwise expressly agreed in writing, each Product shall be covered under the limited warranty by the Company that every Product has been manufactured in accordance with applicable law and that it meets its specifications, it will be free from defects in materials or workmanship, provided it is stored, used and handled under the conditions recommended by Company. The Company warranty is for a period of twelve (12) months from the date of commissioning or eighteen (18) months from the date of dispatch, whichever occurs earlier. In the event of a valid deficiency claim, the Company's sole obligation shall be, at its discretion, to either:\n(i) Repair the defective component(s), or\n(ii) Replace the defective component(s), free of charge, provided that such components are returned to the Company's premises in the original or equivalent protective packaging.\n\nc. The Company shall be liable only for:\n(i) Defects arising from its own design or manufacturing faults; and\n(ii) Material defects that the Company should have reasonably discovered through due diligence.\n\nd. The Company shall not be liable for any claims, losses, or damages arising out of or relating to the following circumstances, whether direct or indirect:\n(i) Normal wear and tear of the Products under regular operating conditions, including deterioration due to environmental exposure, usage, or time;\n(ii) Improper handling, incorrect storage, misuse, negligence, or operation of the Products in a manner inconsistent with the Product specifications, manuals, or any written instructions provided by the Company;\n(iii) Any modification of the Products undertaken by the Customer or any third party;\n(iv) Use of non-original replacement parts, components, or consumables with the Products;\n(v) Any force majeure events including but not limited to fire, flood, act of God, civil unrest, strikes, war, pandemic, or government-imposed restrictions;\n(vi) Consequential or indirect damages including, but not limited to, loss of production, business interruption, penalties for delay, freight costs, costs of disassembly/reassembly, or damage to other machinery or equipment.\n(vii) Any claims arising after the expiration of the applicable warranty period.\n\ne. All other terms and conditions shall be as specified in the Installation and Operating Manual issued by the Company.\n\nf. The Customer represents that it has all the requisite power to execute these Terms and to perform its obligations hereunder, and the person(s) implementing these Terms on its behalf are duly authorised. These Terms are legally binding upon it and it does not conflict with any agreement, instrument or understanding, oral or written, to which it is a party or by which it may be bound."
//   },
//   {
//     title: "9. Indemnity and Limitation of Liability",
//     content: "a. The Customer shall indemnify and hold harmless the Company and its affiliates (\"Indemnified Parties\") from any claims, losses, liabilities, damages, or expenses (including legal fees) arising from:\n(i) any breach of these Terms;\n(ii) any negligence, willful misconduct, or legal violation by the Customer or its representatives;\n(iii) any misuse, unauthorized modification, or improper handling of the Products by the Customer or parties under its control;\n(iv) any claim that Customer-provided specifications, drawings, or instructions infringe third-party intellectual property rights.\n\nb. The Company shall not be liable for any indirect, incidental, consequential, punitive, or special damages, including loss of profits, data, or business, even if advised of such possibility. These limitations and exclusions apply regardless of the form or basis of the claim."
//   },
//   {
//     title: "10. Term and Termination",
//     content: "These Terms shall remain in effect until completion of the obligations by both Parties and may be terminated earlier by mutual written consent or for material breach not remedied within a reasonable period as discussed in writing by the Customer and the Company."
//   },
//   {
//     title: "11. Confidentiality Obligations",
//     content: "The Customer agrees to keep confidential all technical, commercial, and business information received from the Company. The Customer must protect the confidentiality of any information shared by the Company for a period of two (2) years after termination. Breach may result in a fixed penalty (amount to be agreed) per violation, in addition to potential damage claims. The Company also retains the right to claim indemnification of damage caused to it by the disclosure of the information."
//   },
//   {
//     title: "12. Governing Law and Jurisdiction",
//     content: "These Terms are governed by the laws of India. Disputes shall be subject to the exclusive jurisdiction of courts in Pune, Maharashtra, India."
//   }
// ];

// const EditGeneralConditionsModal = ({ isOpen, onClose, onSave, currentConditions }) => {
//   const [conditions, setConditions] = useState(DEFAULT_CONDITIONS);

//   useEffect(() => {
//     if (currentConditions) {
//       parseConditions(currentConditions);
//     }
//   }, [currentConditions]);

//   const parseConditions = (conditionsText) => {
//     if (!conditionsText) return;
    
//     const parsed = [];
//     const lines = conditionsText.split('\n');
//     let currentCondition = null;
    
//     lines.forEach(line => {
//       const titleMatch = line.match(/^(\d+\.\s+.+?):/);
//       if (titleMatch) {
//         if (currentCondition) {
//           parsed.push(currentCondition);
//         }
//         currentCondition = {
//           title: titleMatch[1],
//           content: line.substring(titleMatch[0].length).trim()
//         };
//       } else if (currentCondition && line.trim()) {
//         currentCondition.content += ' ' + line.trim();
//       }
//     });
    
//     if (currentCondition) {
//       parsed.push(currentCondition);
//     }
    
//     if (parsed.length > 0) {
//       setConditions(parsed);
//     }
//   };

//   const handleConditionChange = (index, field, value) => {
//     const newConditions = [...conditions];
//     newConditions[index][field] = value;
//     setConditions(newConditions);
//   };

//   const handleAddCondition = () => {
//     setConditions([...conditions, {
//       title: `${conditions.length + 1}. New Condition`,
//       content: ''
//     }]);
//   };

//   const handleRemoveCondition = (index) => {
//     if (conditions.length === 1) {
//       alert('At least one condition is required');
//       return;
//     }
//     setConditions(conditions.filter((_, i) => i !== index));
//   };

//   const handleSave = async () => {
//     const formattedConditions = conditions.map(c => 
//       `${c.title}: ${c.content}`
//     ).join('\n\n');
    
//     await onSave(formattedConditions);
//     onClose();
//   };

//   const handleResetDefaults = () => {
//     setConditions(DEFAULT_CONDITIONS);
//   };

//   if (!isOpen) return null;

//   return (
//     <div style={styles.overlay}>
//       <div style={styles.modal}>
//         <div style={styles.header}>
//           <h2 style={styles.title}>Edit General Conditions</h2>
//           <button onClick={onClose} style={styles.closeBtn}>×</button>
//         </div>

//         <div style={styles.content}>
//           {conditions.map((condition, index) => (
//             <div key={index} style={styles.conditionBlock}>
//               <div style={styles.conditionHeader}>
//                 <input
//                   type="text"
//                   value={condition.title}
//                   onChange={(e) => handleConditionChange(index, 'title', e.target.value)}
//                   style={styles.titleInput}
//                 />
//                 {conditions.length > 1 && (
//                   <button
//                     onClick={() => handleRemoveCondition(index)}
//                     style={styles.removeBtn}
//                   >
//                     Remove
//                   </button>
//                 )}
//               </div>
//               <textarea
//                 value={condition.content}
//                 onChange={(e) => handleConditionChange(index, 'content', e.target.value)}
//                 style={styles.textarea}
//                 rows="5"
//                 placeholder="Enter condition details..."
//               />
//             </div>
//           ))}

//           <button onClick={handleAddCondition} style={styles.addBtn}>
//             + Add New Condition
//           </button>
//         </div>

//         <div style={styles.footer}>
//           <button onClick={handleResetDefaults} style={styles.resetBtn}>
//             Reset to Defaults
//           </button>
//           <div style={styles.actionBtns}>
//             <button onClick={handleSave} style={styles.saveBtn}>Save</button>
//             <button onClick={onClose} style={styles.cancelBtn}>Cancel</button>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

// const styles = {
//   overlay: {
//     position: 'fixed',
//     top: 0,
//     left: 0,
//     right: 0,
//     bottom: 0,
//     backgroundColor: 'rgba(0,0,0,0.5)',
//     display: 'flex',
//     justifyContent: 'center',
//     alignItems: 'center',
//     zIndex: 1000
//   },
//   modal: {
//     backgroundColor: 'white',
//     borderRadius: '8px',
//     width: '900px',
//     maxHeight: '90vh',
//     display: 'flex',
//     flexDirection: 'column',
//     boxShadow: '0 4px 20px rgba(0,0,0,0.3)'
//   },
//   header: {
//     display: 'flex',
//     justifyContent: 'space-between',
//     alignItems: 'center',
//     padding: '20px',
//     borderBottom: '1px solid #ddd',
//     backgroundColor: '#ff6600'
//   },
//   title: {
//     margin: 0,
//     color: 'white',
//     fontSize: '20px'
//   },
//   closeBtn: {
//     background: 'none',
//     border: 'none',
//     fontSize: '28px',
//     color: 'white',
//     cursor: 'pointer',
//     padding: '0',
//     width: '30px',
//     height: '30px'
//   },
//   content: {
//     padding: '20px',
//     overflowY: 'auto',
//     flex: 1
//   },
//   conditionBlock: {
//     marginBottom: '25px',
//     padding: '20px',
//     border: '1px solid #ddd',
//     borderRadius: '4px',
//     backgroundColor: '#f9f9f9'
//   },
//   conditionHeader: {
//     display: 'flex',
//     justifyContent: 'space-between',
//     alignItems: 'center',
//     marginBottom: '12px'
//   },
//   titleInput: {
//     flex: 1,
//     padding: '10px',
//     fontSize: '15px',
//     fontWeight: 'bold',
//     border: '1px solid #ccc',
//     borderRadius: '4px',
//     marginRight: '10px'
//   },
//   textarea: {
//     width: '100%',
//     padding: '12px',
//     fontSize: '14px',
//     border: '1px solid #ccc',
//     borderRadius: '4px',
//     fontFamily: 'Arial, sans-serif',
//     resize: 'vertical',
//     lineHeight: '1.5'
//   },
//   removeBtn: {
//     padding: '8px 15px',
//     backgroundColor: '#dc3545',
//     color: 'white',
//     border: 'none',
//     borderRadius: '4px',
//     cursor: 'pointer',
//     fontSize: '14px'
//   },
//   addBtn: {
//     padding: '12px 24px',
//     backgroundColor: '#007bff',
//     color: 'white',
//     border: 'none',
//     borderRadius: '4px',
//     cursor: 'pointer',
//     fontSize: '15px',
//     fontWeight: '600',
//     marginTop: '10px'
//   },
//   footer: {
//     padding: '15px 20px',
//     borderTop: '1px solid #ddd',
//     display: 'flex',
//     justifyContent: 'space-between',
//     alignItems: 'center'
//   },
//   resetBtn: {
//     padding: '10px 20px',
//     backgroundColor: '#6c757d',
//     color: 'white',
//     border: 'none',
//     borderRadius: '4px',
//     cursor: 'pointer'
//   },
//   actionBtns: {
//     display: 'flex',
//     gap: '10px'
//   },
//   saveBtn: {
//     padding: '10px 30px',
//     backgroundColor: '#28a745',
//     color: 'white',
//     border: 'none',
//     borderRadius: '4px',
//     cursor: 'pointer',
//     fontSize: '15px'
//   },
//   cancelBtn: {
//     padding: '10px 30px',
//     backgroundColor: '#6c757d',
//     color: 'white',
//     border: 'none',
//     borderRadius: '4px',
//     cursor: 'pointer',
//     fontSize: '15px'
//   }
// };

// export default EditGeneralConditionsModal;