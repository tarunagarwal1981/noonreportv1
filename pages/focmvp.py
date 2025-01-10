import React, { useState, useEffect } from 'react';
import { Card } from "@/components/ui/card";
import { Table } from "@/components/ui/table";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { AlertCircle, Plus, Upload } from 'lucide-react';
import { Alert, AlertDescription } from "@/components/ui/alert";

const TankSoundingForm = () => {
  // State for checkboxes
  const [bunkering, setBunkering] = useState(false);
  const [debunkering, setDebunkering] = useState(false);
  const [bunkerSurvey, setBunkerSurvey] = useState(false);
  const [tankTransfer, setTankTransfer] = useState(false);

  // State for entries
  const [bunkeringEntries, setBunkeringEntries] = useState([{}]);
  const [debankeringEntries, setDebankeringEntries] = useState([{}]);

  // Tank and consumer data
  const tanks = Array.from({length: 8}, (_, i) => `Tank ${i + 1}`);
  const consumers = [
    'Main Engine', 'Aux Engine1', 'Aux Engine2', 'Aux Engine3',
    'Boiler 1', '    Boiler 1 - Cargo Heating', '    Boiler 1 - Discharge',
    'Boiler 2', '    Boiler 2 - Cargo Heating', '    Boiler 2 - Discharge',
    'IGG', 'Incinerator', 'DPP1', 'DPP2', 'DPP3'
  ];

  // Generate initial data
  const generateInitialData = () => {
    const fuelTypes = ["VLSFO", "MGO", "HFO"];
    const bdnNumbers = Array.from({length: 3}, () => 
      Math.random().toString(36).substring(2, 10).toUpperCase()
    );
    
    return tanks.reduce((acc, tank, idx) => {
      acc[tank] = {
        fuelType: fuelTypes[Math.floor(Math.random() * fuelTypes.length)],
        bdnNumber: bdnNumbers[idx % 3],
        previousROB: Math.random() * 900 + 100,
        ...consumers.reduce((c, consumer) => ({
          ...c,
          [consumer]: Math.random() * 50
        }), {}),
        currentROB: 0 // Will be calculated
      };
      return acc;
    }, {});
  };

  const [tankData, setTankData] = useState(generateInitialData());

  // Bunkering Entry Component
  const BunkeringEntry = ({ index }) => (
    <Card className="p-4 mb-4 bg-slate-800/50 border-slate-700/50">
      <h3 className="text-sm font-medium text-slate-200 mb-3">Bunkering Entry {index + 1}</h3>
      <div className="grid grid-cols-3 gap-4">
        <div className="space-y-2">
          <Input placeholder="BDN Number" className="bg-slate-800/80" />
          <Input type="date" className="bg-slate-800/80" />
          <Input type="time" className="bg-slate-800/80" />
          {/* File upload for BDN */}
          <div className="border border-slate-700/50 rounded-md p-2 bg-slate-800/80">
            <label className="text-xs text-slate-400">BDN Upload</label>
            <div className="flex items-center gap-2 mt-1">
              <Input type="file" className="text-xs" accept=".pdf,.jpg,.png" />
              <Upload className="h-4 w-4 text-slate-400" />
            </div>
          </div>
          {/* File upload for Analysis Report */}
          <div className="border border-slate-700/50 rounded-md p-2 bg-slate-800/80">
            <label className="text-xs text-slate-400">Analysis Report Upload</label>
            <div className="flex items-center gap-2 mt-1">
              <Input type="file" className="text-xs" accept=".pdf,.jpg,.png" />
              <Upload className="h-4 w-4 text-slate-400" />
            </div>
          </div>
        </div>
        <div className="space-y-2">
          <Input placeholder="IMO Number" className="bg-slate-800/80" />
          <Input placeholder="Fuel Type" className="bg-slate-800/80" />
          <Input type="number" placeholder="Mass (mt)" min="0" step="0.1" className="bg-slate-800/80" />
        </div>
        <div className="space-y-2">
          <Input type="number" placeholder="Lower heating value (MJ/kg)" className="bg-slate-800/80" />
          <Input type="number" placeholder="EU GHG intensity" className="bg-slate-800/80" />
          <Input type="number" placeholder="IMO GHG intensity" className="bg-slate-800/80" />
        </div>
      </div>
      <div className="mt-4">
        <label className="text-xs text-slate-400">Select Tanks</label>
        <div className="grid grid-cols-4 gap-2 mt-1">
          {tanks.map(tank => (
            <label key={tank} className="flex items-center gap-2">
              <input type="checkbox" className="rounded bg-slate-800/80" />
              <span className="text-sm text-slate-300">{tank}</span>
            </label>
          ))}
        </div>
      </div>
    </Card>
  );

  // Main Tank Data Table
  const TankTable = () => {
    const rows = [
      'Fuel Type',
      'BDN Number',
      'Previous ROB',
      ...consumers,
      ...(bunkering ? ['Bunker Qty (mT)'] : []),
      ...(debunkering ? ['Debunkered Qty (mT)'] : []),
      ...(bunkerSurvey ? ['Survey Qty (mT)'] : []),
      ...(!bunkerSurvey ? ['Current ROB'] : [])
    ];

    return (
      <div className="rounded-md border border-slate-700/50 overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="bg-slate-800/50">
              <th className="p-2 text-left text-sm font-medium text-slate-300">Parameter</th>
              {tanks.map(tank => (
                <th key={tank} className="p-2 text-left text-sm font-medium text-slate-300">
                  {tank}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, idx) => (
              <tr key={row} className="border-t border-slate-700/50">
                <td className="p-2 text-sm text-slate-300">{row}</td>
                {tanks.map(tank => (
                  <td key={`${tank}-${row}`} className="p-2">
                    <Input 
                      type={row.includes('Qty') || row.includes('ROB') ? 'number' : 'text'}
                      className="bg-slate-800/80 h-8 text-sm"
                      value={tankData[tank]?.[row] || ''}
                      onChange={(e) => {
                        const newData = {...tankData};
                        newData[tank] = {...newData[tank], [row]: e.target.value};
                        setTankData(newData);
                      }}
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  return (
    <div className="p-4 space-y-6">
      {/* Operation Type Selection */}
      <Card className="bg-slate-800/50 border-slate-700/50 p-4">
        <div className="grid grid-cols-4 gap-4">
          <label className="flex items-center gap-2">
            <input 
              type="checkbox" 
              checked={bunkering}
              onChange={(e) => setBunkering(e.target.checked)}
              className="rounded bg-slate-800/80"
            />
            <span className="text-sm text-slate-300">Bunkering Record</span>
          </label>
          <label className="flex items-center gap-2">
            <input 
              type="checkbox"
              checked={debunkering}
              onChange={(e) => setDebunkering(e.target.checked)}
              className="rounded bg-slate-800/80"
            />
            <span className="text-sm text-slate-300">Debunkering Record</span>
          </label>
          <label className="flex items-center gap-2">
            <input 
              type="checkbox"
              checked={bunkerSurvey}
              onChange={(e) => setBunkerSurvey(e.target.checked)}
              className="rounded bg-slate-800/80"
            />
            <span className="text-sm text-slate-300">Bunker Survey</span>
          </label>
          <label className="flex items-center gap-2">
            <input 
              type="checkbox"
              checked={tankTransfer}
              onChange={(e) => setTankTransfer(e.target.checked)}
              className="rounded bg-slate-800/80"
            />
            <span className="text-sm text-slate-300">Tank-to-Tank Transfer</span>
          </label>
        </div>
      </Card>

      {/* Bunkering Section */}
      {bunkering && (
        <div className="space-y-4">
          <h2 className="text-lg font-medium text-slate-100">Bunkering Details</h2>
          {bunkeringEntries.map((_, idx) => (
            <BunkeringEntry key={idx} index={idx} />
          ))}
          <Button 
            variant="outline" 
            size="sm" 
            onClick={() => setBunkeringEntries([...bunkeringEntries, {}])}
            className="flex items-center gap-2"
          >
            <Plus className="h-4 w-4" />
            Add Bunkering Entry
          </Button>
        </div>
      )}

      {/* Tank Sounding Table */}
      <div className="space-y-4">
        <h2 className="text-lg font-medium text-slate-100">Tank Sounding Data</h2>
        <TankTable />
      </div>

      {/* Submit Button */}
      <Button type="submit" className="w-full">
        Submit Report
      </Button>
    </div>
  );
};

export default TankSoundingForm;
