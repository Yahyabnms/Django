from django.core.management.base import BaseCommand
from Voiture.models import Voiture
from Location.models import Location
from Reservation.models import Reservation

class Command(BaseCommand):
    help = 'Supprime les voitures en double (même marque et modèle) et garde la plus récente'

    def handle(self, *args, **options):
        # Trouver les doublons par marque et modèle
        voitures = Voiture.objects.all().order_by('marque', 'modele', '-date_ajout')
        
        seen = {}
        to_delete = []
        
        for voiture in voitures:
            key = (voiture.marque, voiture.modele)
            if key in seen:
                to_delete.append(voiture)
                self.stdout.write(
                    self.style.WARNING(
                        f'Doublon trouvé: {voiture.marque} {voiture.modele} (ID: {voiture.id}) - à supprimer'
                    )
                )
            else:
                seen[key] = voiture
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Gardé: {voiture.marque} {voiture.modele} (ID: {voiture.id})'
                    )
                )
        
        if to_delete:
            # Migrer les références avant suppression
            for voiture in to_delete:
                key = (voiture.marque, voiture.modele)
                voiture_garde = seen[key]
                
                # Migrer les locations
                locations_count = Location.objects.filter(voiture=voiture).update(voiture=voiture_garde)
                if locations_count > 0:
                    self.stdout.write(
                        self.style.WARNING(
                            f'  Migré {locations_count} location(s) de {voiture.id} vers {voiture_garde.id}'
                        )
                    )
                
                # Migrer les réservations
                reservations_count = Reservation.objects.filter(voiture=voiture).update(voiture=voiture_garde)
                if reservations_count > 0:
                    self.stdout.write(
                        self.style.WARNING(
                            f'  Migré {reservations_count} réservation(s) de {voiture.id} vers {voiture_garde.id}'
                        )
                    )
            
            # Supprimer les doublons
            count = len(to_delete)
            Voiture.objects.filter(id__in=[v.id for v in to_delete]).delete()
            self.stdout.write(
                self.style.SUCCESS(
                    f'Supprimé {count} voiture(s) en double.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    'Aucun doublon trouvé.'
                )
            )
