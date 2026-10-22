"""
Global Industrial Recycling & ELV Depollution Engine - AI & RWA Protocol
-------------------------------------------------------------------------
Open-Source Web3 & AI Engine for Tokenizing Industrial Recycling Plant CapEx, 
Autonomous Spectroscopic AI Metal Grading, and Smart Payouts for ELVs & Copper.

License: MIT
"""

import time
import hashlib
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class FacilityCapExToken:
    token_id: str
    investor_address: str
    facility_code: str
    amount_funded_eur: float
    equity_yield_share: float
    timestamp: float = field(default_factory=time.time)

@dataclass
class MetalScrapIntake:
    intake_id: str
    supplier_address: str
    metal_category: str  # "Ferrous_Steel", "High_Purity_Copper", "Aluminum", "ELV_Vehicle"
    weight_kg: float
    unit_price_per_kg: float
    total_payout_eur: float
    is_paid: bool = False

@dataclass
class AIRoboticGradingResult:
    scan_id: str
    metal_purity_percent: float
    detected_grade: str
    suggested_lme_market_price_eur: float

class AIRoboticMetalScanner:
    """
    AI Spectroscopic Vision Engine for Automated Metal Grading & Depollution Checks.
    Scans incoming scrap loads to determine copper purity and verify ELV toxic fluid extraction.
    """
    def __init__(self, scanner_id: str, facility_code: str):
        self.scanner_id = scanner_id
        self.facility_code = facility_code

    def analyze_metal_composition(self, metal_type: str, weight_kg: float) -> AIRoboticGradingResult:
        """Simulates AI-driven optical and spectroscopic material identification."""
        scan_id = hashlib.sha256(f"{self.scanner_id}_{time.time()}".encode()).hexdigest()[:10]
        
        if metal_type == "High_Purity_Copper":
            purity = 99.2
            grade = "Cu-Grade-A-Bare-Bright"
            market_price = 8.50  # EUR/kg
        elif metal_type == "Ferrous_Steel":
            purity = 95.0
            grade = "E3-Heavy-Melting-Steel"
            market_price = 0.32  # EUR/kg
        elif metal_type == "ELV_Vehicle":
            purity = 88.0
            grade = "Complete-ELV-Auto-Body"
            market_price = 0.25  # EUR/kg
        else:
            purity = 85.0
            grade = "Mixed-Industrial-Scrap"
            market_price = 0.20  # EUR/kg

        print(f"[AI ROBOTIC SCANNER] ID '{self.scanner_id}': Analyzed {weight_kg}kg of '{metal_type}'. Detected Grade: '{grade}' ({purity}% Purity). LME Rate: €{market_price}/kg")
        
        return AIRoboticGradingResult(
            scan_id=scan_id,
            metal_purity_percent=purity,
            detected_grade=grade,
            suggested_lme_market_price_eur=market_price
        )

class IndustrialRecyclingTokenEngine:
    """
    Real-World Asset (RWA) & AI Engine for Industrial REMAT & Auto Depollution Plants.
    Manages tokenized plant financing, automated metal weighbridge intakes, and instant farmer/supplier payouts.
    """
    def __init__(self, platform_name: str = "GLOBAL-REMAT-RECYCLING-NETWORK"):
        self.platform_name = platform_name
        self.investor_registry: Dict[str, FacilityCapExToken] = {}
        self.scrap_intakes: Dict[str, MetalScrapIntake] = {}
        self.scanners: Dict[str, AIRoboticMetalScanner] = {}
        self.total_capex_raised_eur: float = 0.0
        self.total_scrap_payouts_eur: float = 0.0

    def register_ai_scanner(self, scanner_id: str, facility_code: str) -> AIRoboticMetalScanner:
        """Registers an AI metal grading scanner deployed at a facility."""
        scanner = AIRoboticMetalScanner(scanner_id=scanner_id, facility_code=facility_code)
        self.scanners[scanner_id] = scanner
        print(f"[AI SCANNER REGISTERED] Scanner '{scanner_id}' deployed to Facility '{facility_code}'")
        return scanner

    def fund_facility_capex(self, investor: str, facility_code: str, amount_eur: float, target_capex: float = 500000.0) -> FacilityCapExToken:
        """Allows global impact funds or industrial investors to tokenize REMAT recycling plant openings."""
        token_id = hashlib.sha256(f"{investor}_{facility_code}_{time.time()}".encode()).hexdigest()[:12]
        yield_share = (amount_eur / target_capex) * 100.0

        token = FacilityCapExToken(
            token_id=token_id,
            investor_address=investor,
            facility_code=facility_code,
            amount_funded_eur=amount_eur,
            equity_yield_share=yield_share
        )

        self.investor_registry[token_id] = token
        self.total_capex_raised_eur += amount_eur
        print(f"[CAPEX FUNDED] Investor {investor[:8]}... funded €{amount_eur:,.2f} for Facility '{facility_code}' ({yield_share:.2f}% Yield Share)")
        return token

    def process_scrap_weighbridge_intake(self, supplier: str, metal_type: str, weight_kg: float, scanner_id: str) -> MetalScrapIntake:
        """Processes scrap metal intake via weighbridge and AI grading scanner."""
        if scanner_id in self.scanners:
            scan_result = self.scanners[scanner_id].analyze_metal_composition(metal_type, weight_kg)
            unit_price = scan_result.suggested_lme_market_price_eur
        else:
            unit_price = 0.20

        total_value = weight_kg * unit_price
        intake_id = hashlib.sha256(f"{supplier}_{metal_type}_{time.time()}".encode()).hexdigest()[:10]

        intake = MetalScrapIntake(
            intake_id=intake_id,
            supplier_address=supplier,
            metal_category=metal_type,
            weight_kg=weight_kg,
            unit_price_per_kg=unit_price,
            total_payout_eur=total_value
        )

        self.scrap_intakes[intake_id] = intake
        print(f"[INTAKE LOGGED] Supplier {supplier[:8]}... delivered {weight_kg:,.1f}kg of {metal_type} (€{total_value:,.2f} payable)")
        return intake

    def execute_instant_supplier_payout(self, intake_id: str):
        """Executes instant smart contract payout to scrap supplier or auto owner upon delivery verification."""
        if intake_id not in self.scrap_intakes:
            print(f"[ERROR] Intake ID {intake_id} not found.")
            return

        intake = self.scrap_intakes[intake_id]
        if intake.is_paid:
            print(f"[WARNING] Intake {intake_id} already settled.")
            return

        intake.is_paid = True
        self.total_scrap_payouts_eur += intake.total_payout_eur

        print("\n" + "="*75)
        print(f"      SMART CONTRACT PAYOUT EXECUTED TO SCRAP SUPPLIER")
        print("="*75)
        print(f"Intake ID: {intake_id}")
        print(f"Supplier Address: {intake.supplier_address}")
        print(f"Material Type: {intake.metal_category} ({intake.weight_kg:,.1f} kg)")
        print(f"Total Instant Settlement: €{intake.total_payout_eur:,.2f}")
        print("="*75 + "\n")

    def distribute_monthly_plant_yield(self, facility_code: str, monthly_net_profit_eur: float):
        """Distributes monthly operational net profits to plant RWA token holders."""
        print(f"\n[PLANT PROFIT DISTRIBUTION] Facility '{facility_code}' generated €{monthly_net_profit_eur:,.2f} net profit.")
        print(f"Distributing yield dividends to RWA Token Holders:")

        for tid, token in self.investor_registry.items():
            if token.facility_code == facility_code:
                dividend = monthly_net_profit_eur * (token.equity_yield_share / 100.0)
                print(f" -> Investor {token.investor_address[:8]}... received €{dividend:,.2f} dividend.")

    def print_network_summary(self):
        """Generates executive status report for the global industrial recycling network."""
        print("\n" + "#"*75)
        print(f"      {self.platform_name} - GLOBAL LEDGER & AI REPORT")
        print("#"*75)
        print(f"Total Facility CapEx Crowdfunded: €{self.total_capex_raised_eur:,.2f}")
        print(f"Total Direct Supplier Payouts Executed: €{self.total_scrap_payouts_eur:,.2f}")
        print(f"Total Active AI Metal Scanners: {len(self.scanners)}")
        print(f"Total Registered Facility Investors: {len(self.investor_registry)}")
        print("#"*75 + "\n")


# --- EXECUTION DEMO ---
if __name__ == "__main__":
    engine = IndustrialRecyclingTokenEngine(platform_name="GLOBAL-REMAT-RECYCLING-NETWORK")

    print("\n--- 1. DEPLOYING AI SCANNER & FUNDING REMAT PLANT CAPEX ---")
    scanner = engine.register_ai_scanner("AI-SCANNER-RO-01", "REMAT-RO-CLUJ-01")
    engine.fund_facility_capex("0xGreenFund_Alpha...", "REMAT-RO-CLUJ-01", amount_eur=250000.0, target_capex=500000.0)
    engine.fund_facility_capex("0xCircularImpact_Beta...", "REMAT-RO-CLUJ-01", amount_eur=250000.0, target_capex=500000.0)

    print("\n--- 2. WEIGHBRIDGE SCRAP INTAKE & AI COMPOSITION ANALYSIS ---")
    # Intake 1: High purity copper cables
    intake1 = engine.process_scrap_weighbridge_intake("0xLocalSupplier111...", "High_Purity_Copper", weight_kg=1200.0, scanner_id="AI-SCANNER-RO-01")
    engine.execute_instant_supplier_payout(intake1.intake_id)

    # Intake 2: End-of-Life Vehicle (ELV) Auto Scrapping
    intake2 = engine.process_scrap_weighbridge_intake("0xCarOwner222...", "ELV_Vehicle", weight_kg=1450.0, scanner_id="AI-SCANNER-RO-01")
    engine.execute_instant_supplier_payout(intake2.intake_id)

    print("\n--- 3. MONTHLY PLANT PROFIT YIELD DISTRIBUTION ---")
    engine.distribute_monthly_plant_yield("REMAT-RO-CLUJ-01", monthly_net_profit_eur=25000.0)

    print("\n--- 4. NETWORK LEDGER REPORT ---")
    engine.print_network_summary()
