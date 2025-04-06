from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.utils import parseaddr
import base64
from typing import List
from ..schemas import EmailResponse
import email
from bs4 import BeautifulSoup
import html2text

class GmailService:
    def __init__(self):
        self.api_version = 'v1'
        self.service_name = 'gmail'

    async def get_unread_emails(self, credentials: Credentials) -> List[EmailResponse]:
        """Get unread emails from Gmail"""
        service = build(self.service_name, self.api_version, credentials=credentials)
        
        try:
            # Get list of unread messages
            results = service.users().messages().list(
                userId='me',
                labelIds=['UNREAD'],
                maxResults=5,
                q='in:inbox'  # Solo mensajes en la bandeja de entrada
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            for message in messages:
                # Obtener el mensaje completo con el contenido
                msg = service.users().messages().get(
                    userId='me',
                    id=message['id'],
                    format='full'
                ).execute()
                
                # Obtener información del thread (cadena de correos)
                thread = service.users().threads().get(
                    userId='me',
                    id=msg['threadId']
                ).execute()
                
                # Extraer headers
                headers = msg['payload']['headers']
                email_data = {
                    'from_': '',
                    'subject': '',
                    'date': '',
                    'snippet': msg.get('snippet', ''),
                    'full_content': self._get_message_content(msg['payload']),
                    'thread_messages': []
                }
                
                for header in headers:
                    name = header['name'].lower()
                    value = header['value']
                    
                    if name == 'from':
                        _, email_addr = parseaddr(value)
                        email_data['from_'] = email_addr
                    elif name == 'subject':
                        email_data['subject'] = value
                    elif name == 'date':
                        email_data['date'] = value
                
                # Agregar mensajes del thread
                for thread_message in thread['messages']:
                    if thread_message['id'] != message['id']:  # Evitar duplicar el mensaje principal
                        thread_data = {
                            'from_': '',
                            'date': '',
                            'content': self._get_message_content(thread_message['payload'])
                        }
                        
                        # Extraer headers del mensaje en el thread
                        for header in thread_message['payload']['headers']:
                            name = header['name'].lower()
                            value = header['value']
                            
                            if name == 'from':
                                _, email_addr = parseaddr(value)
                                thread_data['from_'] = email_addr
                            elif name == 'date':
                                thread_data['date'] = value
                        
                        email_data['thread_messages'].append(thread_data)
                
                emails.append(EmailResponse(**email_data))
            
            return emails
            
        except Exception as e:
            raise Exception(f"Error fetching emails: {str(e)}")

    def _get_message_content(self, payload):
        """Extract message content from payload"""
        if 'body' in payload and payload['body'].get('data'):
            # Mensaje simple
            data = payload['body']['data']
            text = base64.urlsafe_b64decode(data).decode()
            return self._clean_html_content(text)
        
        if 'parts' in payload:
            # Mensaje multiparte
            text_content = []
            for part in payload['parts']:
                if part['mimeType'] in ['text/plain', 'text/html']:
                    if 'data' in part['body']:
                        data = part['body']['data']
                        text = base64.urlsafe_b64decode(data).decode()
                        text_content.append(self._clean_html_content(text))
            return '\n'.join(text_content)
        
        return ''

    def _clean_html_content(self, content):
        """Clean HTML content and convert to readable text"""
        try:
            # Intentar parsear como HTML
            soup = BeautifulSoup(content, 'html.parser')
            h = html2text.HTML2Text()
            h.ignore_links = False
            return h.handle(str(soup))
        except:
            # Si falla, devolver el contenido original
            return content 