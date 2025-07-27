from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from io import BytesIO

def generate_user_pdf_report(user, reservations, total_hours, total_cost, total_reservations, most_used_lot, month):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=20,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20,
        alignment=1  # Center aligned
    )
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#3498db'),
        spaceAfter=10
    )
    normal_style = styles['Normal']
    normal_style.textColor = colors.HexColor('#34495e')
    
    # Header with colored box
    c.setFillColor(colors.HexColor('#3498db'))
    c.rect(0, height-60, width, 60, fill=True, stroke=False)
    
    # Title in header
    title = Paragraph("ParkSmart - Monthly Parking Report", title_style)
    title.wrapOn(c, width-100, 50)
    title.drawOn(c, 50, height-50)
    
    # Report month below header
    month_text = Paragraph(f"Report for {month}", ParagraphStyle(
        'MonthStyle',
        parent=normal_style,
        fontSize=12,
        textColor=colors.white,
        alignment=1
    ))
    month_text.wrapOn(c, width-100, 20)
    month_text.drawOn(c, 50, height-80)
    
    # User Details in a card-like layout
    c.setFillColor(colors.HexColor('#ecf0f1'))
    c.rect(30, height-180, width-60, 100, fill=True, stroke=False)
    
    user_title = Paragraph("User Information", heading_style)
    user_title.wrapOn(c, width-100, 20)
    user_title.drawOn(c, 40, height-140)
    
    user_data = [
        [f"Name: {user.username}", f"Email: {user.email}"],
        [f"Vehicle: {user.vehicles[0].vehicle_number if user.vehicles else 'N/A'} ({user.vehicles[0].vehicle_type if user.vehicles else 'N/A'})", 
         f"Address: {user.address or 'N/A'}, {user.pin_code or 'N/A'}"]
    ]
    
    user_table = Table(user_data, colWidths=[width/2-60, width/2-60])
    user_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#2c3e50'))
    ]))
    user_table.wrapOn(c, width-100, 60)
    user_table.drawOn(c, 40, height-170)
    
    # Summary in a grid layout
    summary_title = Paragraph("Parking Summary", heading_style)
    summary_title.wrapOn(c, width-100, 20)
    summary_title.drawOn(c, 40, height-300)
    
    summary_data = [
        ["Total Reservations", str(total_reservations)],
        ["Total Hours Parked", f"{round(total_hours, 2)} hrs"],
        ["Total Cost", f"Rs.{round(total_cost, 2)}"],
        ["Most Visited Lot", most_used_lot]
    ]
    
    summary_table = Table(summary_data, colWidths=[width/2-60, width/2-60])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#ecf0f1')),
        ('GRID', (0,0), (-1,-1), 1, colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('BOLD', (0,0), (-1,0), 1)
    ]))
    summary_table.wrapOn(c, width-100, 100)
    summary_table.drawOn(c, 40, height-380)
    
    # Reservation Details
    details_title = Paragraph("Recent Reservations", heading_style)
    details_title.wrapOn(c, width-100, 20)
    details_title.drawOn(c, 40, height-450)
    
    # Prepare reservation data
    res_data = [["Date", "Time", "Spot", "Duration", "Cost"]]
    for r in reservations[:20]:
        date = r.reserved_at.strftime('%d %b %Y') if r.reserved_at else "N/A"
        time_range = (
            f"{r.reserved_at.strftime('%Y-%m-%d %H:%M')} - {r.reserved_till.strftime('%Y-%m-%d %H:%M')}"
            if r.reserved_at and r.reserved_till
            else "N/A"
        )

        spot = f"Spot {r.spot_id}" if r.spot_id else "Unknown"
        duration = f"{round((r.reserved_till - r.reserved_at).total_seconds()/3600, 1)}h" if r.reserved_at and r.reserved_till else "N/A"
        cost = f"Rs.{r.parking_cost:.2f}" if r.parking_cost else "Rs.0.00"
        res_data.append([date, time_range, spot, duration, cost])
    
    res_table = Table(res_data, colWidths=[width/5-10]*5, repeatRows=1)
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#2c3e50')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    
    # Handle multi-page tables
    available_height = height - 500
    required_height = len(reservations[:20]) * 20 + 40  # Approximate row height
    
    if required_height > available_height:
        # Split table across pages
        res_table.wrapOn(c, width-80, available_height)
        res_table.drawOn(c, 40, height-500)
        c.showPage()
        res_table = Table(res_data[len(reservations[:10])+1:], colWidths=[width/5-10]*5)
        res_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTSIZE', (0,0), (-1,-1), 9),
            ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
            ('BACKGROUND', (0,1), (-1,-1), colors.white),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#2c3e50')),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
        ]))
        res_table.wrapOn(c, width-80, height-100)
        res_table.drawOn(c, 40, height-100)
    else:
        res_table.wrapOn(c, width-80, available_height)
        res_table.drawOn(c, 40, height-500)
    
    # Footer
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor('#7f8c8d'))
    c.drawCentredString(width/2, 30, "Thank you for using ParkSmart - Your trusted parking solution")
    
    c.save()
    buffer.seek(0)
    return buffer.read()







def generate_admin_pdf_report(admin_user, reservations_by_user, reservations_by_lot, total_hours, total_cost, month):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontSize=20,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=20,
        alignment=1
    )
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#3498db'),
        spaceAfter=10
    )
    subheading_style = ParagraphStyle(
        'SubheadingStyle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=8
    )
    normal_style = styles['Normal']
    normal_style.textColor = colors.HexColor('#34495e')

    # Header with colored box
    c.setFillColor(colors.HexColor('#3498db'))
    c.rect(0, height-60, width, 60, fill=True, stroke=False)
    
    # Title in header
    title = Paragraph("ParkSmart - Admin Monthly Report", title_style)
    title.wrapOn(c, width-100, 50)
    title.drawOn(c, 50, height-50)
    
    # Report month below header
    month_text = Paragraph(f"Report for {month}", ParagraphStyle(
        'MonthStyle',
        parent=normal_style,
        fontSize=12,
        textColor=colors.white,
        alignment=1
    ))
    month_text.wrapOn(c, width-100, 20)
    month_text.drawOn(c, 50, height-80)

    # Admin info section
    c.setFillColor(colors.HexColor('#ecf0f1'))
    c.rect(30, height-180, width-60, 80, fill=True, stroke=False)
    
    admin_title = Paragraph("Admin Information", heading_style)
    admin_title.wrapOn(c, width-100, 20)
    admin_title.drawOn(c, 40, height-150)
    
    admin_data = [
        [f"Name: {admin_user.username}", f"Email: {admin_user.email}"],
        [f"Report Generated: {datetime.now().strftime('%d %b %Y %H:%M')}", ""]
    ]
    
    admin_table = Table(admin_data, colWidths=[width/2-60, width/2-60])
    admin_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.HexColor('#2c3e50'))
    ]))
    admin_table.wrapOn(c, width-100, 40)
    admin_table.drawOn(c, 40, height-180)

    # Summary section
    summary_title = Paragraph("Parking Summary", heading_style)
    summary_title.wrapOn(c, width-100, 20)
    summary_title.drawOn(c, 40, height-280)
    
    summary_data = [
        ["Total Revenue", f"Rs.{round(total_cost, 2)}"],
        ["Total Parking Hours", f"{round(total_hours, 2)} hrs"],
        ["Total Users", str(len(reservations_by_user))],
        ["Total Parking Lots", str(len(reservations_by_lot))]
    ]
    
    summary_table = Table(summary_data, colWidths=[width/2-60, width/2-60])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#ecf0f1')),
        ('GRID', (0,0), (-1,-1), 1, colors.lightgrey),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('BOLD', (0,0), (-1,0), 1)
    ]))
    summary_table.wrapOn(c, width-100, 100)
    summary_table.drawOn(c, 40, height-360)

    # Reservations by User
    user_title = Paragraph("Reservations by User", heading_style)
    user_title.wrapOn(c, width-100, 20)
    user_title.drawOn(c, 40, height-440)
    
    user_data = [["User", "Reservations", "Hours", "Revenue"]]
    for user, reservations in reservations_by_user.items():
        user_hours = sum((r.reserved_till - r.reserved_at).total_seconds()/3600 
                        for r in reservations if r.reserved_at and r.reserved_till)
        user_revenue = sum(r.parking_cost for r in reservations if r.parking_cost)
        user_data.append([
            user,
            str(len(reservations)),
            f"{round(user_hours, 1)} hrs",
            f"Rs.{round(user_revenue, 2)}"
        ])
    
    user_table = Table(user_data, colWidths=[width*0.4, width*0.2, width*0.2, width*0.2], repeatRows=1)
    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#2c3e50')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    
    # Handle pagination for user table
    available_height = height - 480
    required_height = len(reservations_by_user) * 15 + 40
    
    if required_height > available_height:
        user_table.wrapOn(c, width-80, available_height)
        user_table.drawOn(c, 40, height-480)
        c.showPage()
        # Draw remaining user data if needed
    else:
        user_table.wrapOn(c, width-80, available_height)
        user_table.drawOn(c, 40, height-480)

    # Reservations by Lot
    lot_title = Paragraph("Reservations by Parking Lot", heading_style)
    lot_title.wrapOn(c, width-100, 20)
    lot_title.drawOn(c, 40, height-50 if required_height > available_height else height-480-required_height-30)
    
    lot_data = [["Parking Lot", "Reservations", "Hours", "Revenue"]]
    for lot, reservations in reservations_by_lot.items():
        lot_hours = sum((r.reserved_till - r.reserved_at).total_seconds()/3600 
                    for r in reservations if r.reserved_at and r.reserved_till)
        lot_revenue = sum(r.parking_cost for r in reservations if r.parking_cost)
        lot_data.append([
            lot,
            str(len(reservations)),
            f"{round(lot_hours, 1)} hrs",
            f"Rs.{round(lot_revenue, 2)}"
        ])
    
    lot_table = Table(lot_data, colWidths=[width*0.4, width*0.2, width*0.2, width*0.2], repeatRows=1)
    lot_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#3498db')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), colors.white),
        ('TEXTCOLOR', (0,1), (-1,-1), colors.HexColor('#2c3e50')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    
    # Handle pagination for lot table
    lot_table.wrapOn(c, width-80, height-100)
    lot_table.drawOn(c, 40, height-100)

    # Footer
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.HexColor('#7f8c8d'))
    c.drawCentredString(width/2, 30, "ParkSmart Administration - Confidential Report")
    
    c.save()
    buffer.seek(0)
    return buffer.read()